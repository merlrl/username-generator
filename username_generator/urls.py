from django.urls import path
from . import views

urlpatterns = [
    # 1. /generate-username
    path('generate-username/', views.generate_username, name='generate-username'),

    # 2. /check-username
    path('check-username/', views.check_username, name='check-username'),

    # 3. /username-suggestions
    path('username-suggestions/', views.username_suggestions, name='username-suggestions'),

    # 4. /username-length
    path('username-length/', views.username_length, name='username-length'),

    # 5. /username-complexity
    path('username-complexity/', views.username_complexity, name='username-complexity'),

    # 6. /username-availability
    path('username-availability/', views.username_availability, name='username-availability'),

    # 7. /username-from-phrase
    path('username-from-phrase/', views.username_from_phrase, name='username-from-phrase'),

    # 8. /similar-username-suggestions
    path('similar-username-suggestions/', views.similar_username_suggestions, name='similar-username-suggestions'),

    # 9. /prefix-username
    path('prefix-username/', views.prefix_username, name='prefix-username'),

    # 10. /suffix-username
    path('suffix-username/', views.suffix_username, name='suffix-username'),

    # 11. /username-history
    path('username-history/', views.username_history, name='username-history'),

    # 12. /username-feedback/<int:id>
    path('username-feedback/<int:id>/', views.username_feedback, name='username-feedback'),

    # 13. /avoid-special-characters
    path('avoid-special-characters/', views.avoid_special_characters, name='avoid-special-characters'),

    # 14. /username-variation
    path('username-variation/', views.username_variation, name='username-variation'),

    # 15. /filter-inappropriate-words
    path('filter-inappropriate-words/', views.filter_inappropriate_words, name='filter-inappropriate-words'),

    # 16. /custom-username
    path('custom-username/', views.custom_username, name='custom-username'),

    # 17. /random-username-idea
    path('random-username-idea/', views.random_username_idea, name='random-username-idea'),

    # 18. /username-suggestions-by-hobby
    path('username-suggestions-by-hobby/', views.username_suggestions_by_hobby, name='username-suggestions-by-hobby'),

    # 19. /username-check-similarity
    path('username-check-similarity/', views.username_check_similarity, name='username-check-similarity'),

    # 20. /username-history-summary
    path('username-history-summary/', views.username_history_summary, name='username-history-summary'),
]
