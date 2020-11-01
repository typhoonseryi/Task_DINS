# API  https://mtricht.github.io/diabotical-api/#/Leaderboard/get_api_v0_stats_leaderboard
# Command-line приложение leaderboard.py позволяет:
1) Получать информацию (все поля, кроме user_id) об N пользователях игрового режима mode построчно в формате json.  python ./leaderboard.py --mode <MODE> --count N
2) Получать инофрмацию (все поля, кроме user_id) о пользователе игрового режима mode с определенным user_id.  python ./leaderboard.py --mode <MODE> --count N --user_id <user_id>
3) Получать информацию о количестве пользователей определенной страны в выборке.  python ./leaderboard.py --mode <MODE> --count N --country ru
