# baseball_matching/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db import transaction
from .models import Game, Position, UserProfile, PointHistory, UsedItem
from .forms import GameForm, ProfileForm, UsedItemForm

# HTTP 요청을 처리하고 응답을 반환하는 로직
# 비즈니스 로직의 핵심

# views.py
from django.utils import timezone
from django.db.models import Count

def main(request):
    # 현재 날짜 이후의 모집 중인 경기들을 날짜순으로 가져옴
    current_games = Game.objects.filter(
        date__gte=timezone.now().date(),
        status='RECRUITING'
    ).order_by('date', 'time')

    # 각 경기별 남은 포지션 수 계산
    for game in current_games:
        filled_positions = Position.objects.filter(
            game=game,
            is_filled=True
        ).count()
        # 전체 포지션 수(18) - 채워진 포지션 수 = 남은 포지션 수
        game.remaining_positions = 18 - filled_positions

    return render(request, 'baseball_matching/main.html', {
        'current_games': current_games
    })

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, '회원가입이 완료되었습니다!')
#             return redirect('baseball_matching:main')
#     else:
#         form = UserCreationForm()
#     return render(request, 'baseball_matching/register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # UserProfile은 signals.py에서 자동 생성되므로 여기서는 생성하지 않음

            # 로그인 처리
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username,
                                password=raw_password,
                                backend='django.contrib.auth.backends.ModelBackend')
            if user is not None:
                login(request, user)
                messages.success(request, '회원가입이 완료되었습니다!')
                return redirect('baseball_matching:main')
    else:
        form = UserCreationForm()
    return render(request, 'baseball_matching/register.html', {'form': form})



# @login_required
# def profile(request):
#     return render(request, 'baseball_matching/profile.html', {
#         'user_profile': request.user.userprofile
#     })

@login_required
def profile(request):
    # 사용자가 참가 중인 포지션들 가져오기
    user_positions = Position.objects.filter(
        player=request.user.userprofile,
        is_filled=True
    ).select_related('game')

    # 사용자가 등록한 판매물품들 가져오기
    user_items = UsedItem.objects.filter(
        seller=request.user.userprofile
    ).order_by('-created_at')  # 최신순으로 정렬

    context = {
        'user': request.user,
        'user_positions': user_positions,
        'user_items': user_items  # 템플릿에 전달할 판매물품 목록 추가
    }
    return render(request, 'baseball_matching/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
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

@login_required
def change_item_status(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(UsedItem, id=item_id, seller=request.user.userprofile)
        new_status = request.POST.get('status')
        if new_status in dict(UsedItem.STATUS_CHOICES):
            item.status = new_status
            item.save()
    return redirect('baseball_matching:used_item_detail', item_id=item_id)


@login_required
def game_edit(request, game_id):
    game = get_object_or_404(Game, id=game_id, creator=request.user.userprofile)

    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, '경기가 수정되었습니다.')
            return redirect('baseball_matching:game_detail', game_id=game.id)
    else:
        form = GameForm(instance=game)

    return render(request, 'baseball_matching/game_form.html', {
        'form': form,
        'title': '경기 수정',
        'is_edit': True
    })


@login_required
def game_delete(request, game_id):
    game = get_object_or_404(Game, id=game_id, creator=request.user.userprofile)

    if request.method == 'POST':
        game.delete()
        messages.success(request, '경기가 삭제되었습니다.')
        return redirect('baseball_matching:game_list')

    return render(request, 'baseball_matching/game_delete_confirm.html', {'game': game})


@login_required
def used_item_edit(request, item_id):
    item = get_object_or_404(UsedItem, id=item_id, seller=request.user.userprofile)

    if request.method == 'POST':
        form = UsedItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, '물품이 수정되었습니다.')
            return redirect('baseball_matching:used_item_detail', item_id=item.id)
    else:
        form = UsedItemForm(instance=item)

    return render(request, 'baseball_matching/used_item_form.html', {
        'form': form,
        'is_edit': True
    })


@login_required
def used_item_delete(request, item_id):
    item = get_object_or_404(UsedItem, id=item_id, seller=request.user.userprofile)

    if request.method == 'POST':
        item.delete()
        messages.success(request, '물품이 삭제되었습니다.')
        return redirect('baseball_matching:used_item_list')

    return render(request, 'baseball_matching/used_item_delete_confirm.html', {'item': item})

@login_required
def game_create(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.creator = request.user.userprofile
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

# views.py에 추가
@login_required
def used_item_list(request):
    items = UsedItem.objects.filter(is_sold=False).order_by('-created_at')
    return render(request, 'baseball_matching/used_item_list.html', {'items': items})

@login_required
def used_item_create(request):
    if request.method == 'POST':
        form = UsedItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user.userprofile
            item.save()
            messages.success(request, '상품이 등록되었습니다.')
            return redirect('baseball_matching:used_item_list')
    else:
        form = UsedItemForm()
    return render(request, 'baseball_matching/used_item_form.html', {'form': form})

@login_required
def used_item_detail(request, item_id):
    item = get_object_or_404(UsedItem, id=item_id)
    item.views += 1
    item.save()
    return render(request, 'baseball_matching/used_item_detail.html', {'item': item})


@login_required
def used_item_detail(request, item_id):
    item = get_object_or_404(UsedItem, id=item_id)
    return render(request, 'baseball_matching/used_item_detail.html', {
        'item': item
    })

@login_required
def chat_room(request, seller_id):
    seller = get_object_or_404(UserProfile, id=seller_id)
    return render(request, 'baseball_matching/chat_room.html', {
        'seller': seller
    })