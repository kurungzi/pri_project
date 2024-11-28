# baseball_matching/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db import transaction
from .models import Game, Position, UserProfile, PointHistory
from .forms import GameForm, ProfileForm

# HTTP 요청을 처리하고 응답을 반환하는 로직
# 비즈니스 로직의 핵심

def main(request):
    return render(request, 'baseball_matching/main.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '회원가입이 완료되었습니다!')
            return redirect('baseball_matching:main')
    else:
        form = UserCreationForm()
    return render(request, 'baseball_matching/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'baseball_matching/profile.html', {
        'user_profile': request.user.userprofile
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필이 수정되었습니다.')
            return redirect('baseball_matching:profile')
    else:
        form = ProfileForm(instance=request.user.userprofile)
    return render(request, 'baseball_matching/edit_profile.html', {'form': form})


@login_required # 로그인 안된 상태에서 호출시 에러
def game_list(request):
    games = Game.objects.filter(status='RECRUITING').order_by('date', 'time')
    return render(request, 'baseball_matching/game_list.html', {'games': games})


@login_required
def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    home_positions = Position.objects.filter(game=game, team='HOME')
    away_positions = Position.objects.filter(game=game, team='AWAY')

    context = {
        'game': game,
        'home_positions': home_positions,
        'away_positions': away_positions,
    }
    return render(request, 'baseball_matching/game_detail.html', context)


# @login_required
# def game_create(request):
#     if request.method == 'POST':
#         form = GameForm(request.POST)
#         if form.is_valid():
#             game = form.save(commit=False)
#             game.save()
#
#             # 포지션 자동 생성
#             positions = ['P', 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']
#             for team in ['HOME', 'AWAY']:
#                 for pos in positions:
#                     Position.objects.create(
#                         game=game,
#                         team=team,
#                         position=pos
#                     )
#
#             messages.success(request, '경기가 성공적으로 등록되었습니다.')
#             return redirect('baseball_matching:game_detail', game_id=game.id)
#     else:
#         form = GameForm()
#
#     return render(request, 'baseball_matching/game_form.html', {
#         'form': form,
#         'title': '새 경기 등록'
#     })

@login_required
def game_create(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.status = 'RECRUITING'  # 초기 상태 설정
            game.save()

            # 포지션 자동 생성
            positions = ['P', 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']
            for team in ['HOME', 'AWAY']:
                for pos in positions:
                    Position.objects.create(
                        game=game,
                        team=team,
                        position=pos
                    )

            messages.success(request, '경기가 성공적으로 등록되었습니다.')
            return redirect('baseball_matching:game_detail', game_id=game.id)
    else:
        form = GameForm()

    return render(request, 'baseball_matching/game_form.html', {
        'form': form,
        'title': '새 경기 등록'
    })

@login_required
@transaction.atomic
def join_position(request, position_id):
    position = get_object_or_404(Position, id=position_id)
    user_profile = request.user.userprofile

    existing_position = Position.objects.filter(
        game=position.game,
        player=user_profile
    ).exists()

    if position.is_filled:
        messages.error(request, '이미 마감된 포지션입니다.')
        return redirect('baseball_matching:game_detail', game_id=position.game.id)

    if user_profile.points < position.game.participation_fee:
        messages.error(request, '포인트가 부족합니다.')
        return redirect('baseball_matching:game_detail', game_id=position.game.id)

    # 포인트 차감 및 포지션 할당
    user_profile.points -= position.game.participation_fee
    user_profile.save()

    if existing_position:
        messages.error(request, '이미 이 경기에 다른 포지션을 신청하셨습니다.')
        return redirect('baseball_matching:game_detail', game_id=position.game.id)

    # 포인트 사용 내역 기록
    PointHistory.objects.create(
        user=user_profile,
        amount=-position.game.participation_fee,
        transaction_type='USE',
        description=f'{position.game.title} - {position.get_position_display()} 참가'
    )

    position.player = user_profile
    position.is_filled = True
    position.save()

    messages.success(request, '포지션 신청이 완료되었습니다.')
    return redirect('baseball_matching:game_detail', game_id=position.game.id)


@login_required
@transaction.atomic
def cancel_position(request, position_id):
    position = get_object_or_404(Position, id=position_id)

    # 자신의 포지션인지 확인
    if position.player != request.user.userprofile:
        messages.error(request, '본인이 신청한 포지션만 취소할 수 있습니다.')
        return redirect('baseball_matching:game_detail', game_id=position.game.id)

    # 포인트 환불
    user_profile = request.user.userprofile
    refund_amount = position.game.participation_fee
    user_profile.points += refund_amount
    user_profile.save()

    # 환불 내역 기록
    PointHistory.objects.create(
        user=user_profile,
        amount=refund_amount,
        transaction_type='REFUND',
        description=f'{position.game.title} - {position.get_position_display()} 신청 취소'
    )

    # 포지션 초기화
    position.player = None
    position.is_filled = False
    position.save()

    messages.success(request, f'신청이 취소되었고 {refund_amount}P가 환불되었습니다.')
    return redirect('baseball_matching:game_detail', game_id=position.game.id)


@login_required
def charge_points(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 0))
        if amount > 0:
            # 트랜잭션 처리로 데이터 일관성 보장
            with transaction.atomic():
                # 사용자 프로필 업데이트
                user_profile = request.user.userprofile
                user_profile.points += amount
                user_profile.save()

                # 충전 내역 기록
                PointHistory.objects.create(
                    user=user_profile,
                    amount=amount,
                    transaction_type='CHARGE',
                    description='포인트 충전'
                )

            # 성공 메시지 표시
            messages.success(request, f'{amount:,}포인트가 충전되었습니다.')
            # 메인 페이지로 리다이렉트
            return redirect('baseball_matching:main')

    return render(request, 'baseball_matching/charge_points.html') # 충전 시 홈으로 돌아가게끔 경로 수정


@login_required
def point_history(request):
    histories = PointHistory.objects.filter(
        user=request.user.userprofile
    ).order_by('-created_at')

    return render(request, 'baseball_matching/point_history.html', {
        'point_history': histories
    })