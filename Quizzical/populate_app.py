import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Quizzical.settings')

import django
django.setup()

from django.contrib.auth.models import User
from app.models import UserProfile, Category, Quiz, Slide, Answer, StarRating

def populate():
    """
    Create a 'system user' + 'system user profile', then populate
    Categories, Quizzes, Slides, Answers, and StarRatings.
    """

    # 1. Create or get a Django User
    system_user, created_user = User.objects.get_or_create(
        username='system_user',
        defaults={
            'email': 'admin@fakeemail.co.uk',
            # This sets an unusable password by default. 
            # We'll overwrite it below with set_password.
        }
    )
    # Update/set a real password
    system_user.set_password('password')
    system_user.save()

    # Create an additional user: 'test' with password 'test'
    test_user, _ = User.objects.get_or_create(username='test', defaults={'email': 'test@example.com'})
    test_user.set_password('test')
    test_user.save()

    # Create or get UserProfile for 'test'
    UserProfile.objects.get_or_create(user=test_user, defaults={'email': test_user.email})

    # 2. Create or get a matching UserProfile
    system_profile, created_profile = UserProfile.objects.get_or_create(
        user=system_user,
        defaults={
            'email': system_user.email,
        }
    )

    # 3. Define the quiz data to be created
    #    You can freely modify names, questions, and answers as needed.
    quiz_data = {
        'General Knowledge': {
            'is_fun': True,
            'quizzes': [
                {
                    'name': 'Quiz 1',
                    'views': 10,
                    'stars': 1,
                    'image': 'quiz1.jpg',  # located in static/images/quiz1.jpg
                    'questions': [
                        {
                            'question': 'What is the largest planet in our solar system?',
                            'answers': [
                                ('Earth', False),
                                ('Jupiter', True),
                                ('Mars', False),
                                ('Saturn', False),
                            ],
                        },
                        {
                            'question': 'Which element has the chemical symbol "O"?',
                            'answers': [
                                ('Oxygen', True),
                                ('Osmium', False),
                                ('Ozone', False),
                                ('Oganesson', False),
                            ],
                        },
                    ],
                },
            ],
        },
        'Entertainment': {
            'is_fun': True,
            'quizzes': [
                {
                    'name': 'Quiz 2',
                    'views': 20,
                    'stars': 2,
                    'image': 'quiz2.jpg',
                    'questions': [
                        {
                            'question': 'Who sang the hit song "Thriller"?',
                            'answers': [
                                ('Michael Jackson', True),
                                ('Elvis Presley', False),
                                ('Prince', False),
                                ('Madonna', False),
                            ],
                        },
                        {
                            'question': 'What is the longest-running TV show in the United States?',
                            'answers': [
                                ('Friends', False),
                                ('The Office', False),
                                ('Grey\'s Anatomy', False),
                                ('The Simpsons', True),
                            ],
                        },
                    ],
                },
            ],
        },
        'Science': {
            'is_fun': False,
            'quizzes': [
                {
                    'name': 'Quiz 3',
                    'views': 30,
                    'stars': 3,
                    'image': 'quiz3.jpg',
                    'questions': [
                        {
                            'question': 'What gas do plants absorb from the atmosphere for photosynthesis?',
                            'answers': [
                                ('Nitrogen', False),
                                ('Oxygen', False),
                                ('Carbon Dioxide', True),
                                ('Hydrogen', True),
                            ],
                        },
                        {
                            'question': 'What is the main function of white blood cells?',
                            'answers': [
                                ('Carry oxygen', False),
                                ('Produce hormones', False),
                                ('Help digestion', False),
                                ('Fight infections', True),
                            ],
                        },
                    ],
                },
            ],
        },
        'History': {
            'is_fun': False,
            'quizzes': [
                {
                    'name': 'Quiz 4',
                    'views': 40,
                    'stars': 4,
                    'image': 'quiz4.jpg',
                    'questions': [
                        {
                            'question': 'Who was the first woman to fly solo across the Atlantic Ocean?',
                            'answers': [
                                ('Amelia Earhart', True),
                                ('Bessie Coleman', False),
                                ('Jacqueline Cochran', False),
                                ('Harriet Quimby', False),
                            ],
                        },
                        {
                            'question': 'Which ancient civilization built the pyramids?',
                            'answers': [
                                ('Romans', False),
                                ('Mayans', False),
                                ('Greeks', False),
                                ('Egyptians', True),
                            ],
                        },
                    ],
                },
                {
                    'name': 'Quiz 5',
                    'views': 50,
                    'stars': 5,
                    'image': 'quiz5.jpg',
                    'questions': [
                        {
                            'question': 'In which year did the Titanic sink?',
                            'answers': [
                                ('1912', True),
                                ('1920', False),
                                ('1898', False),
                                ('1934', False),
                            ],
                        },
                        {
                            'question': 'Who was the British Prime Minister during World War II?',
                            'answers': [
                                ('Winston Churchill', True),
                                ('Neville Chamberlain', False),
                                ('Harold Wilson', False),
                                ('Clement Attlee', False),
                            ],
                        },
                    ],
                },
            ],
        },
    }

    # 4. Create Categories, Quizzes, Slides, Answers, and Star Ratings
    for category_name, category_info in quiz_data.items():
        cat = add_category(
            name=category_name,
            is_fun=category_info['is_fun'],
            created_by=system_profile
        )
        for quiz_info in category_info['quizzes']:
            quiz = add_quiz(
                category=cat,
                name=quiz_info['name'],
                views=quiz_info['views'],
                image=quiz_info['image'],
                created_by=system_profile
            )
            # Add star rating if "stars" is given
            if 'stars' in quiz_info and quiz_info['stars'] > 0:
                add_star_rating(quiz, system_profile, quiz_info['stars'])
            
            # Add slides and answers
            for question_data in quiz_info['questions']:
                slide = add_slide(quiz, question_data['question'])
                for ans_text, ans_correct in question_data['answers']:
                    add_answer(slide, ans_text, ans_correct)

    print("Database population complete.")

def add_category(name, is_fun, created_by):
    """
    Create or get a Category by name and is_fun status.
    """
    category, created = Category.objects.get_or_create(
        name=name,
        defaults={'is_fun': is_fun, 'created_by': created_by}
    )
    if not created:
        # If the category already exists, ensure fields are up to date
        category.is_fun = is_fun
        category.created_by = created_by
        category.save()
    return category

def add_quiz(category, name, views, image, created_by):
    """
    Create or get a Quiz with the specified data.
    """
    quiz, created = Quiz.objects.get_or_create(
        name=name,
        category=category,
        defaults={
            'views': views,
            'image': image,
            'created_by': created_by,
        }
    )
    if not created:
        # If quiz already exists, update any fields if needed
        quiz.views = views
        quiz.image = image
        quiz.created_by = created_by
        quiz.save()
    return quiz

def add_slide(quiz, question):
    """
    Create or get a Slide (question) for the given quiz.
    """
    slide, created = Slide.objects.get_or_create(
        quiz=quiz,
        question=question
    )
    return slide

def add_answer(slide, text, is_correct):
    """
    Create or get an Answer for the given slide.
    """
    answer, created = Answer.objects.get_or_create(
        slide=slide,
        text=text,
        defaults={'is_correct': is_correct}
    )
    if not created:
        # If the answer already exists, ensure is_correct is updated
        answer.is_correct = is_correct
        answer.save()
    return answer

def add_star_rating(quiz, profile, stars):
    """
    Create or get a StarRating for the given quiz and user profile.
    """
    rating, created = StarRating.objects.get_or_create(
        quiz=quiz,
        profile=profile,
        defaults={'stars': stars}
    )
    if not created:
        rating.stars = stars
        rating.save()
    return rating


if __name__ == '__main__':
    print('Starting Quizzical population script...')
    populate()
    print('Done.')
