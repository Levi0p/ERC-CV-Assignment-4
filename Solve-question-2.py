import cv2
import mediapipe as mp
import random

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

width, height = 1280, 640
player_pos = [width // 2, height - 60]
enemy_speed = 5
enemy_size = 50
enemy_list = []
score = 0

def create_enemy():
    x_pos = random.randint(0, width - enemy_size)
    return [x_pos, 0]  # [x, y]

def move_enemies(enemy_list):
    for enemy in enemy_list:
        enemy[1] += enemy_speed

def check_off_screen(enemy_list):
    global score
    for enemy in enemy_list[:]:
        if enemy[1] > height:
            enemy_list.remove(enemy)
            score += 1

def check_collision(player_pos, enemy_list):
    player_x, player_y = player_pos
    player_size = 60
    
    for enemy in enemy_list:
        enemy_x, enemy_y = enemy
        if (player_x < enemy_x + enemy_size and
            player_x + player_size > enemy_x and
            player_y < enemy_y + enemy_size and
            player_y + player_size > enemy_y):
            return True
    return False

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            player_pos[0] = int(index_tip.x * width) - 30
            
            player_pos[0] = max(0, min(player_pos[0], width - 60))

    if random.randint(1, 30) == 1:
        enemy_list.append(create_enemy())
    
    move_enemies(enemy_list)

    if check_collision(player_pos, enemy_list):
        print("Game Over! Your score:", score)
        break

    check_off_screen(enemy_list)

    frame = cv2.rectangle(frame, (player_pos[0], player_pos[1]), (player_pos[0] + 60, player_pos[1] + 60), (0, 255, 0), -1)
    
    for enemy in enemy_list:
        frame = cv2.rectangle(frame, (enemy[0], enemy[1]), (enemy[0] + enemy_size, enemy[1] + enemy_size), (0, 0, 255), -1)

    cv2.putText(frame, f'Score: {score}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Object Dodging Game", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
