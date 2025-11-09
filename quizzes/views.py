from django.shortcuts import render, redirect, get_object_or_404
from .models import*

# Create your views here.

def home(request):
    return render(request, 'home.html')


def quiz_list(request):
    quizzes = Quiz.objects.all()
    con = {"quizzes" : quizzes}
    return render(request, 'quiz_list.html', con)


def quiz_attempt(request, quiz_id):
    # this line retrieves a Quiz object from the database using get_object_or_404() shortcut function
    quiz = get_object_or_404(Quiz, id = quiz_id)

    """
    When you fetch all questions for this quiz, also fetch 
    their answers in advance — in a single additional query.
    """
    questions = quiz.questions_set.prefetch_related('answers_set')

    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        score = 0
        submission = UserSubmission.objects.create(quiz = quiz, user_name = user_name, score=0)

        for q in questions:
            selected_id = request.POST.get(str(q.id))
            if selected_id:
                selected_answer = Answers.objects.get(id=selected_id)
                correct = selected_answer.is_correct
                if correct:
                    score += 1
                UserAnswer.objects.create(
                    submission=submission,
                    question=q,
                    answer=selected_answer,
                    is_correct=correct
                )
        submission.score = score
        submission.save()
        return redirect('quiz_result', submission.id)
    
    con = {'quiz': quiz, 'questions': questions}
    return render(request, 'quiz_attempt.html', con)


def quiz_result(request, submission_id):
    submission = get_object_or_404(UserSubmission, id = submission_id)
    con = {'submission': submission}
    return render(request, 'quiz_result.html', con)