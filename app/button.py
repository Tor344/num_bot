from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = InlineKeyboardMarkup(inline_keyboard=
                                      [[InlineKeyboardButton(text="Прогноз на сегодня",callback_data="forecast")],
                                      [InlineKeyboardButton(text="Выбрать дату",callback_data="choice_date")],
                                      [InlineKeyboardButton(text="Ежедневная подписка на прогноз",callback_data="subscription_date")]]
                                            )


subscription_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Подписался",callback_data="examination")]])

beck_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад",callback_data="beck")]])


un_newsletter_keyboard = InlineKeyboardMarkup(inline_keyboard=
                                      [[InlineKeyboardButton(text="Отписаться",callback_data="unsubscribe")],
                                      [InlineKeyboardButton(text="Назад",callback_data="beck")]])

newsletter_keyboard = InlineKeyboardMarkup(inline_keyboard=
                                      [[InlineKeyboardButton(text="Подписаться",callback_data="subscription_date")],
                                      [InlineKeyboardButton(text="Назад",callback_data="beck")]])


ph_or_text_keyboard = InlineKeyboardMarkup(inline_keyboard=
                                      [[InlineKeyboardButton(text="Фото",callback_data="photo")],
                                      [InlineKeyboardButton(text="Текст",callback_data="text")]])