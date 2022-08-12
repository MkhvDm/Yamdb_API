# from django.db import models
# from django.contrib.auth import get_user_model

# from django.core.validators import MaxValueValidator, MinValueValidator

# User = get_user_model()


# class Review(models.Model):
#     """Модель рецензии на произведение."""
#     title = models.ForeignKey(
#         Title,
#         on_delete=models.CASCADE,
#         related_name='reviews'
#     )
#     text = models.TextField()
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='reviews'
#     )
#     score = models.SmallIntegerField(
#         validators=[
#             MaxValueValidator(10),
#             MinValueValidator(1)
#         ]
#     )
#     pub_date = models.DateTimeField('Дата рецензии', auto_now_add=True)


# class Comment(models.Model):
#     """Модель комментария к рецензии."""
#     review = models.ForeignKey(
#         Review,
#         on_delete=models.CASCADE,
#         related_name='comments'
#     )
#     text = models.TextField()
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='comments'
#     )
#     pub_date = models.DateTimeField('Дата комментария', auto_now_add=True)
