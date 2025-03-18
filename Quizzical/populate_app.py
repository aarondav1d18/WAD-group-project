import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE',
#                     'tango_with_django_project.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Quizzical.settings')

import django
from app.models import *

django.setup()
system_user = UserProfile.objects.create(
    username = "system_user",
    email = "admin@fakeemail.co.uk",
    password = "password",
)
# from app.models import
def populate():    
     
    fun = {
        "General Knowledge": [
            {
                "name" : "Quiz 1",
                "views" : 10,
                "stars" : 1,
                "questions" : [
                    {
                        "question" : "What is the largest planet in our solar system?",
                        "answers" : [
                            ("Earth",False),
                            ("Jupiter",True),
                            ("Mars",False),
                            ("Saturn",False)
                            ],
                    },
                    {
                        "question" : " Which element has the chemical symbol \"O\"?",
                        "answers" : [
                            ("Oxygen", True),
                            ("Osmium", False),
                            ("Ozone", False),
                            ("Oganesson", False),
                        ],
                    },
                ],
            },
        ],

        "Entertainment" : [
            {
                "name" : "Quiz 2",
                "views" : 20,
                "stars" : 2,
                "questions" : [
                    {
                        "question" : "Who sang the hit song \"Thriller\"?",
                        "answers" : [
                            ("Michael Jackson", True),
                            ("Elvis Presley", False),
                            ("Prince", False),
                            ("Madonna", False),
                        ],
                    },
                    {
                        "question" : "What is the longest-running TV show in the United States?",
                        "answers" : [
                            ("Friends", False),
                            ("The Office", False),
                            ("Grey's Anatomy", False),
                            ("The Simpsons", True),
                        ],
                    },
                ],
            },
        ],
    }

    educational = {
        "Science" : [
            {
                "name" : "Quiz 3",
                "views" : 30,
                "stars" : 3,
                "questions" : [
                    {
                        "question" : "What gas do plants absorb from the atmosphere for photosynthesis?",
                        "answers" : [
                            ("Nitrogen", False),
                            ("Oxygen", False),
                            ("Carbon Dioxide", True),
                            ("Hydrogen", True),
                        ],
                    },
                    {
                        "question" : "What is the main function of white blood cells?",
                        "answers" : [
                            ("Carry oxygen", False),
                            ("Produce hormones", False),
                            ("Help digestion", False),
                            ("Fight infections", True),
                        ],
                    },
                ],
            },
        ],

        "History" : [
            {
                "name" : "Quiz 4",
                "views" : 40,
                "stars" : 4,
                "questions" : [
                    {
                        "question" : "Who was the first woman to fly solo across the Atlantic Ocean",
                        "answers" : [
                            ("Amelia Earhart", False),
                            ("Bessie Coleman", False),
                            ("Amelia Earhart", True),
                            ("Jacqueline Cochran", True),
                        ],
                    },
                    {
                        "question" : "Which ancient civilization built the pyramids?",
                        "answers" : [
                            ("Romans", False),
                            ("Mayans", True),
                            ("Greeks", False),
                            ("Egyptians", False),
                        ],
                    },
                ],
            },
            {
                "name" : "Quiz 5",
                "views" : 50,
                "stars" : 5,
                "questions" : [
                    {
                        "question" : "In which year did the Titanic sink?",
                        "answers" : [
                            ("1912", True),
                            ("1920", False),
                            ("1898", False),
                            ("1934", True),
                        ],
                    },
                    {
                        "question" : "Who was the British Prime Minister during World War II?",
                        "answers" : [
                            ("Winston Churchill", False),
                            ("Neville Chamberlain", False),
                            ("Harold Wilson", True),
                            ("Clement Attlee", False),
                        ],
                    },
                ],
            },
        ]
    }

    for category, quizzes in fun.items():
        cat_obj = add_cat(category, True)
        for quiz in quizzes:
            quiz_obj = add_quiz(
                    cat=cat_obj,
                    name=quiz["name"],
                    views=quiz["views"],
                    )
            add_rating(quiz=quiz_obj, stars=quiz["stars"])
            for slide in quiz["questions"]:
                slide_obj = add_slide(quiz=quiz_obj, question=slide["question"])
                for text, is_correct in slide["answers"]:
                    add_answer(slide=slide_obj, text=text, is_correct=is_correct)



def add_cat(name, is_fun):
    c = Category.objects.create(name=name, is_fun=is_fun, created_by=system_user)
    c.save()
    return c

def add_quiz(cat, name, views): 
    q = Quiz.objects.create(
                                category=cat,
                                name=name,
                                views=views,
                                created_by=system_user,
                                )
    q.save()
    return q

def add_slide(quiz, question): # Example questions have not been set with images
    s = Slide.objects.create(quiz=quiz, question=question)
    s.save()
    return s

def add_answer(slide, text, is_correct):
    a = Answer.objects.create(slide=slide, text=text, is_correct=is_correct)
    a.save()
    
def add_rating(quiz, stars):
    s = StarRating.objects.create(quiz=quiz, stars=stars, profile=system_user)
    s.save()    

if __name__ == '__main__':
    print('Starting Quizzical population script...')
    populate()