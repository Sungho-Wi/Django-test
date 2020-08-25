from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
# from django.http import HttpResponse
from .models import Question
from .forms import QuestionForm


# Create your views here.

def index(request):
    # return HttpResponse('안녕하세요 pybo에 오신걸 환영합니다.')

    page = request.GET.get('page', 1)

    question_list = Question.objects.order_by('-create_date')

    kw = request.GET.get('kw', '')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) | # 제목검색
            Q(content__icontains=kw) # 내용검색
        ).distinct()

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 자세한 내용 출력
    """
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('pybo:detail', question_id=question_id)


def question_create(request):
    """
    pybo 질문등록
    """
    if request.method == 'POST':
        print(request.POST)
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()

    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
