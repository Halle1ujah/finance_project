from django.shortcuts import render, redirect, get_object_or_404
from .forms import TransactionForm
from .models import Transaction
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('date')
    daily_data = transactions.values('date').annotate(total=Sum('amount'))
    categories = transactions.values('category').annotate(total=Sum('amount'))
    labels = [item['date'].strftime('%Y-%m-%d') for item in daily_data]
    totals = [float(item['total']) for item in daily_data]  
    category_labels = [item['category'] for item in categories]
    category_totals = [float(item['total']) for item in categories]  
    return render(request, 'finance/dashboard.html', {
        'labels': labels,
        'totals': totals,
        'category_labels': category_labels,
        'category_totals': category_totals,
        'transactions': transactions,
    })
@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'finance/add_transaction.html', {'form': form})
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'finance/signup.html', {'form': form})
@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    transaction.delete()  
    return redirect('dashboard')
def logout_view(request):
    if request.method == 'POST':
        logout(request)  
        return redirect('login')  
    return render(request, 'finance/logout_confirm.html')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # フォームデータを取得
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # メール送信
            subject = f'Inquiry from {name}'
            body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            send_mail(
                subject,
                body,
                'ooi2472042@stu.o-hara.ac.jp',  # 送信元
                ['ooi2472042@stu.o-hara.ac.jp'],   # 受信先
            )

            # 成功メッセージ
            messages.success(request, 'メールが送信されました')
            form = ContactForm()  # 空のフォームを再表示
    else:
        form = ContactForm()

    return render(request, 'finance/contact.html', {'form': form})
