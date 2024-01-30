import json
import random

class Game:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.user_data = self.load_user_data()
        self.current_location = self.user_data.get('current_location', 'start')
        self.game_state = self.user_data.get('game_state', {})

    def load_user_data(self):
        try:
            with open('user.json', 'r') as f:
                user_data = json.load(f)
                return user_data.get(str(self.chat_id), {})
        except FileNotFoundError:
            return {}

    def save_user_data(self):
        with open('user.json', 'r+') as f:
            user_data = json.load(f)
            user_data[str(self.chat_id)] = {
                'current_location': self.current_location,
                'game_state': self.game_state
            }
            f.seek(0)
            json.dump(user_data, f, indent=4)
            f.truncate()

    def roll_dice(self):
        return random.randint(1, 6)

    def start_game(self):
        self.current_location = 'start'
        self.game_state = {}
        self.save_user_data()

    def reset_game(self):
        self.current_location = 'start'
        self.game_state = {}
        self.save_user_data()

    def handle_action(self, action):
        if self.current_location == 'taverna' and action == "Уйти с миром":
            self.current_location = 'start'
            self.save_user_data()
            return "Вы вернулись в город"
        elif self.current_location == 'start' and action == 'Исследовать лес':
            self.current_location = 'forest'
            self.save_user_data()
            return "Вы вошли в темный лес. Вы видите старую дорогу, возможно,она ведет в город. Что будете делать?"
        elif self.current_location == 'start' and action == 'Поговорить с местными жителями':
            self.current_location = 'start'
            self.save_user_data()
            return ("Вы опрашивали местных жителях и узнали, что в подземелье за городом находится артефакт,"
                    " который спасет весь мир от неизбежной гибели")
        elif self.current_location == 'start' and action == 'Посетить таверну':
            self.current_location = 'taverna'
            self.save_user_data()
            return 'Вы посетили таверну'

        elif self.current_location == 'taverna' and action == 'ВЫПИТЬ':
            self.start_game()
            return ('Вы посетили таверну.. Нажрались, поскользнулись на разлитом эле и разбили голову.'
                    '\nИмея такой опыт, начните игру заново и соблюдайте здоровый образ жизни)')

        elif self.current_location == 'forest' and action == 'Пойти в город':
            self.current_location = 'town'
            self.save_user_data()
            return "По тропинке вы вышли к городу. Ваши действия?"
        elif self.current_location == 'forest' and action == 'Сразиться с волками':
            if self.roll_dice() > 3:
                self.current_location = 'town'
                self.save_user_data()
                return 'Вы победили волков и продвинулись в город'
            else:
                self.start_game()  # Пользователь проиграл, и игра начинается заново
                return 'Вы споткнулись об корни деревьев, и волки разорвали вас. Игра закончена. Начните заново.'

        elif self.current_location == 'town' and action == 'Посетить рынок':
            self.current_location = 'Rinok'
            self.save_user_data()
            return 'Вы пришли на городской рынок. Ваши действия?'

        elif self.current_location == 'Rinok' and action == 'Расспросить торговцев о подземелье':
            self.current_location = 'Rinok2'
            self.save_user_data()
            return 'Вам рассказали как добраться до темного подземелья'
        elif self.current_location == 'Rinok' and action == 'Купить рыбки':
            self.current_location = 'town'
            self.save_user_data()
            return ('Вы в панике ищите свой кошелек, чтобы заплатить за вкуснопахнущую рыбку, но не находите его'
                    'поэтому вас выгнали с рынка.\nВаши действия?')
        elif self.current_location == 'Rinok2' and action == 'Пойти в темное подземелье':
            self.current_location = 'dungeon'
            self.save_user_data()
            return 'Вы направились в подземелье'

        elif self.current_location == 'dungeon' and action == 'Попробовать проскользнуть мимо':
            if self.roll_dice() > 2:
                self.current_location = 'end'
                self.save_user_data()
                return ('Вы смогли проскользнуть мимо!'
                        ' Вы вошли в подземелье и видите пред собой большой зАмок,'
                        ' зайдя в него, вы поднялись на верхний этаж.'
                        '\nОткрыв первую попавшуюся вам дверь, вы видите блестящий шар, видимо это и есть артефакт.'
                        '\nВозвращайтесь в город и решите судьбу этого мира!')
            else:
                self.start_game()
                return 'Вас заметили стражи. В попытках убежать, вам прилетает топор в голову и крошит вам череп...'
        elif self.current_location == 'dungeon' and action == 'Сразиться с стражами':
            self.current_location = 'end'
            self.save_user_data()
            return ('Вы с легкостью побеждаете стражей и заходите в подземный зАмок'
                    '\nПоднявшись по лестнице, вы входите в единственную комнату и видите блестящий шар'
                    '\nНу чтож, считай победа, вернувшись в город вы видите нечто..'
                    '\nПеред вам встал трудный выбор')

        elif self.current_location == 'end' and action == 'Использовать артефакт для спасения города':
            self.current_location = 'final'
            self.save_user_data()
            return "Вы разумно активировали артефакт, что привело к уничтожению всей нечисти"
        elif self.current_location == 'end' and action == 'Убежать и спастись':
            self.start_game()
            return 'Вы убежали с поля боя и оставили свой мир умирать... начните все сначала и подумайте хорошенько'

        elif self.current_location == 'end' and action == 'Сразиться с тёмным магом':
            self.current_location = 'final'
            self.save_user_data()
            return ('Вы начинаете сражаться с темным магом...'
                    '\nНаносите первый удар, и падаете замертво..'
                    '\nОказывается он владеет магией мгновенной смерти. Благо вы успели применить артефакт,'
                    'который уничтожил всю нечисть, тем самым, вы стали героем для всего мира!')
        elif self.current_location == 'final' and action == "Интересный квест))":
            self.start_game()
            return "Ты можешь снова его пройти) там есть приколюхи"



        self.save_user_data()