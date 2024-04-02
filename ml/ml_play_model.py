import pygame
import os
from joblib import load

# load the model from ../models/model.pkl using joblib
model = load('./models/model.pkl')

class MLPlay:
    def __init__(self, ai_name,*args,**kwargs):
        self.player_no = ai_name
        self.r_sensor_value = 0
        self.l_sensor_value = 0
        self.f_sensor_value = 0
        self.l_t_sensor_value = 0
        self.r_t_sensor_value = 0
        self.control_list = {"left_PWM": 0, "right_PWM": 0}

        self.training_data = []
        self.frame = 0
        self.passed = False
        
        # Access the LEVEL from the game_params
        self.map = kwargs['game_params']['map']
        print(f"Current Level: {self.map}")

    def update(self, scene_info: dict, keyboard: list = [], *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_ALIVE":
            # get the features from the scene_info
            features = [scene_info["F_sensor"], scene_info["L_sensor"], scene_info["L_T_sensor"], scene_info["R_sensor"], scene_info["R_T_sensor"], scene_info["end_x"], scene_info["end_y"]]
            # predict the control list using the model
            control_list = model.predict([features])[0]
            self.control_list["left_PWM"] = control_list[0]
            self.control_list["right_PWM"] = control_list[1]

            return self.control_list

        self.passed = (scene_info["status"] == "GAME_PASS")
        self.frame = scene_info["frame"]
        return "RESET"

    def reset(self):
        """
        Reset the status
        """
        directory = "./models/win_rate/"
        os.makedirs(directory, exist_ok=True)  # Create directory if it does not exist
        file_path = f"{directory}/win_rate.txt"

        # 如果過關，將訓練資料寫入檔案
        if self.passed:
            print('win')
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('win\n')
        else:
            print('lose')
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('win\n')

        self.passed = False
        self.training_data = []



# scene_info有什麼資料
# {
#     "frame": 16,                # 第幾幀
#     "status": "GAME_ALIVE",     # 遊戲狀態
#     "x": 107.506,               # 車子X座標
#     "y": -112.5,                # 車子Y座標
#     "angle": 0.0,               # 車子角度(float, 0 >= degree > 360)
#     "R_sensor": 5.6,            # 右探測器偵測出的距離
#     "L_sensor": 4.7,            # 左探測器偵測出的距離
#     "F_sensor": 87.6,           # 前探測器偵測出的距離
#     "L_T_sensor": 15.5,           # 左前探測器偵測出的距離
#     "R_T_sensor": 15.8,           # 右前探測器偵測出的距離
#     "end_x": 12.5,              # 終點的X座標
#     "end_y": -12.5              # 終點的Y座標
# }