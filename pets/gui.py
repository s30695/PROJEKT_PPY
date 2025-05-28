import sys, os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QLineEdit, QSpinBox, QStackedWidget, QGridLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt, QTimer

from .controllers import PetController
from .factory import AnimalFactory

# mapowanie polskich nazw pokoi na pliki tła
ROOM_FILES = {
    'Kuchnia':    'kitchen.png',
    'Łazienka':   'bathroom.png',
    'Sala zabaw': 'playroom.png',
    'Sypialnia':  'bedroom.png',
}

class PetSimulatorGUI(QWidget):
    def __init__(self):
        super().__init__()
        # by odbierać zdarzenia klawiatury
        self.setFocusPolicy(Qt.StrongFocus)
        self.ctrl = PetController()
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.assets_animals = os.path.join(base, 'assets', 'animals')
        self.assets_rooms   = os.path.join(base, 'assets', 'rooms')
        self.assets_icons   = os.path.join(base, 'assets', 'icons')
        self.init_ui()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.switch_room(-1)
        elif event.key() == Qt.Key_Right:
            self.switch_room(1)
        else:
            super().keyPressEvent(event)

    def init_ui(self):
        self.setWindowTitle('Symulator Zwierzaka')
        self.resize(800, 600)
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Strony: menu i gra
        self.stack = QStackedWidget()
        self.stack.addWidget(self.create_menu_page())
        self.stack.addWidget(self.create_game_page())
        main_layout.addWidget(self.stack)
        self.show()

    def create_menu_page(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(QLabel('Wybierz zwierzaka:'))
        self.menu_species_cb = QComboBox()
        self.menu_species_cb.addItems(['Pies', 'Kot', 'Królik', 'Chomik'])
        layout.addWidget(self.menu_species_cb)

        # Podgląd avatara w menu
        self.menu_avatar = QLabel()
        self.menu_avatar.setFixedSize(100, 100)
        self.menu_avatar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.menu_avatar)

        layout.addWidget(QLabel('Podaj imię:'))
        self.menu_name_input = QLineEdit()
        layout.addWidget(self.menu_name_input)

        play_btn = QPushButton('Graj')
        play_btn.clicked.connect(self.start_game)
        layout.addWidget(play_btn, alignment=Qt.AlignCenter)

        # Aktualizacja avatara
        self.menu_species_cb.currentIndexChanged.connect(self.update_menu_avatar)
        self.update_menu_avatar()
        return w

    def update_menu_avatar(self):
        species = self.menu_species_cb.currentText()
        icon_filename = AnimalFactory._map[species]('temp').icon_filename
        pix = QPixmap(os.path.join(self.assets_animals, icon_filename))
        self.menu_avatar.setPixmap(
            pix.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

    def create_game_page(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(5)

        # Nawigacja między pokojami
        nav = QHBoxLayout()
        left_btn = QPushButton(); left_btn.setIcon(QIcon(os.path.join(self.assets_icons, 'arrow_left.png')))
        left_btn.clicked.connect(lambda: self.switch_room(-1))
        right_btn = QPushButton(); right_btn.setIcon(QIcon(os.path.join(self.assets_icons, 'arrow_right.png')))
        right_btn.clicked.connect(lambda: self.switch_room(1))
        self.room_label = QLabel('Kuchnia')
        nav.addWidget(left_btn)
        nav.addStretch()
        nav.addWidget(self.room_label)
        nav.addStretch()
        nav.addWidget(right_btn)
        layout.addLayout(nav)

        # Podgląd pokoju (tło + avatar)
        self.room_stack = QStackedWidget()
        self.icon_labels = {}
        for room in ['Kuchnia', 'Łazienka', 'Sala zabaw', 'Sypialnia']:
            page = QWidget()
            vbox = QVBoxLayout(page)
            vbox.setContentsMargins(0, 0, 0, 0)
            vbox.setSpacing(2)

            # Tło i avatar warstwowo
            container = QWidget()
            container.setFixedHeight(300)
            grid = QGridLayout(container)
            grid.setContentsMargins(0, 0, 0, 0)

            bg = QLabel()
            pix_bg = QPixmap(os.path.join(self.assets_rooms, ROOM_FILES[room]))
            bg.setPixmap(pix_bg)
            bg.setScaledContents(True)
            grid.addWidget(bg, 0, 0)

            icon_lbl = QLabel(container)
            icon_lbl.setAlignment(Qt.AlignCenter)
            icon_lbl.setFixedSize(150, 150)
            grid.addWidget(icon_lbl, 0, 0, alignment=Qt.AlignCenter)
            self.icon_labels[room] = icon_lbl

            vbox.addWidget(container)
            self.room_stack.addWidget(page)
        layout.addWidget(self.room_stack)

        # Imię zwierzaka
        self.name_label = QLabel('', alignment=Qt.AlignCenter)
        self.name_label.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(self.name_label)
        # większy odstęp przed wskaźnikami
        layout.addSpacing(15)

        # Wskaźniki stanu bliżej dolnej krawędzi
        layout.addStretch()
        stats = QHBoxLayout()
        stats.setSpacing(10)
        self.hunger_label = QLabel('Głód: –'); stats.addWidget(self.hunger_label)
        self.bored_label  = QLabel('Nuda: –'); stats.addWidget(self.bored_label)
        self.clean_label  = QLabel('Czystość: –'); stats.addWidget(self.clean_label)
        self.energy_label = QLabel('Energia: –'); stats.addWidget(self.energy_label)
        layout.addLayout(stats)

        # Panel akcji
        self.action_stack = QStackedWidget()
        for room in ['Kuchnia', 'Łazienka', 'Sala zabaw', 'Sypialnia']:
            page = QWidget()
            hbox = QHBoxLayout(page)
            if room == 'Kuchnia':
                self.food_spin = QSpinBox(); self.food_spin.setRange(1, 100); self.food_spin.setValue(10)
                btn = QPushButton('Nakarm'); btn.clicked.connect(self.feed_pet)
                hbox.addWidget(QLabel('Ilość:')); hbox.addWidget(self.food_spin); hbox.addWidget(btn)
            elif room == 'Łazienka':
                btn = QPushButton('Umyj'); btn.clicked.connect(self.clean_pet); hbox.addWidget(btn)
            elif room == 'Sala zabaw':
                self.play_spin = QSpinBox(); self.play_spin.setRange(1, 120); self.play_spin.setValue(30)
                btn = QPushButton('Pobaw się'); btn.clicked.connect(self.play_pet)
                hbox.addWidget(QLabel('Czas (s):')); hbox.addWidget(self.play_spin); hbox.addWidget(btn)
            elif room == 'Sypialnia':
                self.sleep_spin = QSpinBox(); self.sleep_spin.setRange(1, 180); self.sleep_spin.setValue(60)
                btn = QPushButton('Śpij'); btn.clicked.connect(self.sleep_pet)
                hbox.addWidget(QLabel('Czas (min):')); hbox.addWidget(self.sleep_spin); hbox.addWidget(btn)
            self.action_stack.addWidget(page)
        layout.addWidget(self.action_stack)

        self.current_room = 0
        return w

    def start_game(self):
        name = self.menu_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, 'Brak imienia', 'Proszę podać imię zwierzęcia.')
            return
        species = self.menu_species_cb.currentText()
        self.ctrl.select_pet(species, name)
        self.stack.setCurrentIndex(1)
        self.update_labels()
        self.timer = QTimer(); self.timer.timeout.connect(self.game_tick); self.timer.start(1000)

    def switch_room(self, delta):
        self.current_room = (self.current_room + delta) % self.room_stack.count()
        self.room_stack.setCurrentIndex(self.current_room)
        self.action_stack.setCurrentIndex(self.current_room)
        names = ['Kuchnia', 'Łazienka', 'Sala zabaw', 'Sypialnia']
        self.room_label.setText(names[self.current_room])
        self.update_labels()

    def update_labels(self):
        s = self.ctrl.get_state()
        self.name_label.setText(self.ctrl.pet.name)
        self.hunger_label.setText(f'Głód: {s.hunger}')
        self.bored_label.setText(f'Nuda: {s.bored}')
        self.clean_label.setText(f'Czystość: {s.clean}')
        self.energy_label.setText(f'Energia: {s.energy}')
        room = ['Kuchnia', 'Łazienka', 'Sala zabaw', 'Sypialnia'][self.current_room]
        icon_lbl = self.icon_labels[room]
        pix = QPixmap(os.path.join(self.assets_animals, self.ctrl.pet.icon_filename))
        icon_lbl.setPixmap(pix.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def feed_pet(self):
        s = self.ctrl.pet.state
        s.hunger = min(100, s.hunger + self.food_spin.value())
        s.clamp(); self.update_labels()

    def play_pet(self):
        s = self.ctrl.pet.state
        s.bored = min(100, s.bored + self.play_spin.value())
        s.clamp(); self.update_labels()

    def clean_pet(self):
        self.ctrl.clean_pet(); self.update_labels()

    def sleep_pet(self):
        self.ctrl.sleep_pet(self.sleep_spin.value()); self.update_labels()

    def game_tick(self):
        self.ctrl.tick(); self.update_labels()
        s = self.ctrl.get_state()
        if s.hunger <= 0 or s.bored <= 0 or s.clean <= 0 or s.energy <= 0:
            QMessageBox.information(self, 'Koniec gry', f"{self.ctrl.pet.name} nie przeżył. Gra zakończona.")
            self.timer.stop(); self.stack.setCurrentIndex(0)


def main():
    app = QApplication(sys.argv); gui = PetSimulatorGUI(); sys.exit(app.exec_())
