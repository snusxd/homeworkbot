import datetime

from netschoolapi import NetSchoolAPI, errors
from config.config import NS_URL, SCHOOL_ID, GROUP_CREDENTIALS

async def fetch_homework_for_group(group_name: str) -> str:
    credentials = GROUP_CREDENTIALS.get(group_name)
    if not credentials:
        return f"Не найдены учётные данные для группы '{group_name}'!"

    user_name = credentials["login"]
    password = credentials["password"]

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%d.%m.%Y")

    async with NetSchoolAPI(NS_URL) as api:
        try:
            await api.login(
                user_name=user_name,
                password=password,
                school_name_or_id=SCHOOL_ID,
                requests_timeout=30
            )
        except errors.NoResponseFromServer:
            return "Ошибка: сервер СГО не отвечает при входе. Попробуйте позже."
        except errors.AuthError as e:
            return f"Ошибка авторизации: {e}"
        except Exception as e:
            return f"Неизвестная ошибка при авторизации: {e}"

        try:
            diary = await api.diary(
                start=tomorrow,
                end=tomorrow,
                requests_timeout=30
            )
        except errors.NoResponseFromServer:
            return "Ошибка: сервер СГО не отвечает при запросе дневника. Попробуйте позже."
        except Exception as e:
            return f"Ошибка при получении дневника: {e}"

        schedule = getattr(diary, "schedule", None)
        if not schedule:
            return "На завтра нет заданий, наслаждайся отдыхом!"

        homework_lines = []

        for day_info in schedule:
            lessons = getattr(day_info, "lessons", [])
            for i, lesson in enumerate(lessons, start=1):
                subject = getattr(lesson, "subject", "Без названия")
                assignments = getattr(lesson, "assignments", [])

                for assignment in assignments:
                    if getattr(assignment, "type", "") == "Домашнее задание":
                        content = getattr(assignment, "content", "")
                        line = f"{i}. {subject}: {content}"
                        homework_lines.append(line)

    if not homework_lines:
        return "На завтра нет заданий, наслаждайся отдыхом!"

    header = (
        f"<b>ДОМАШНЕЕ ЗАДАНИЕ НА <u>{tomorrow_str}</u></b>\n"
        f"<b>{group_name}:</b>\n\n"
    )
    body = "\n".join(homework_lines)

    return header + body