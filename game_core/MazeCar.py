import math

from mlgame.view.test_decorator import check_game_progress, check_game_result
from mlgame.view.view_model import create_text_view_data, create_asset_init_data, create_image_view_data, \
    create_line_view_data, Scene, create_polygon_view_data, create_rect_view_data
from mlgame.gamedev.game_interface import PaiaGame
from .mazeMode import MazeMode
from .moveMazeMode import MoveMazeMode
from .practiceMode import PracticeMode
from .sound_controller import *

'''need some fuction same as arkanoid which without dash in the name of fuction'''

class MazeCar(PaiaGame):
    def __init__(self, user_num, game_type, map, time, sensor, sound):
        super().__init__()
        self.maze_id = map - 1
        self.game_end_time = time
        self.is_sound = sound
        if game_type == "MAZE":
            self.game_mode = MazeMode(user_num, map, time, sensor, self.is_sound)
            self.game_type = "MAZE"
        elif game_type == "MOVE_MAZE":
            self.game_mode = MoveMazeMode(user_num,map,time, sensor, self.is_sound)
            self.game_type = "MOVE_MAZE"

        elif game_type == "PRACTICE":
            self.game_mode = PracticeMode(user_num,map,time, sensor, self.is_sound)
            self.game_type = "PRACTICE"
        self.user_num = user_num
        self.game_mode.sound_controller.play_music()
        self.is_running = self.isRunning()
        self.map_width = self.game_mode.map.width
        self.map_height = self.game_mode.map.height
        self.scene = Scene(WIDTH, HEIGHT, "#000000", 500 - self.map_width, 480 - self.map_height)

    def update(self, cmd_dict):
        # self.game_mode.ticks()
        self.game_mode.handle_event()
        self.game_mode.update_sprite(cmd_dict)
        if not self.isRunning():
            return "QUIT"

    def game_to_player_data(self):
        scene_info = self.get_scene_info
        player_info = {}
        for car in self.game_mode.car_info:
            # type of car is dictionary
            player_info["ml_" + str(car["id"] + 1) + "P"] = {"frame": scene_info["frame"],
                                                             "status": scene_info["status"],
                                                             "x": car["coordinate"][0],
                                                             "y": car["coordinate"][1],
                                                             "angle": (car["angle"] * 180 / math.pi) % 360,
                                                             "R_sensor": car["r_sensor_value"]["distance"],
                                                             "L_sensor": car["l_sensor_value"]["distance"],
                                                             "F_sensor": car["f_sensor_value"]["distance"],
                                                             "L_T_sensor": car["l_t_sensor_value"]["distance"],
                                                             "R_T_sensor": car["r_t_sensor_value"]["distance"],
                                                             "end":self.game_mode.end_point.get_info()["coordinate"]}
        return player_info

    def reset(self):
        pass

    def isRunning(self):
        return self.game_mode.isRunning()

    @property
    def get_scene_info(self):
        """
        Get the scene information
        """
        scene_info = {
            "frame": self.game_mode.frame,
            "status": self.game_mode.status,
        }

        for car in self.game_mode.car_info:
            # type of car is dictionary
            scene_info[str(car["id"]) + "P_position"] = car["topleft"]
        return scene_info

    def get_scene_init_data(self) -> dict:
        """
        Get the scene and object information for drawing on the web
        """
        game_info = {"scene": self.scene.__dict__,
                     "assets":[]}
        game_info["map_width"] = self.game_mode.map.tileWidth * 20
        game_info["map_height"] =self.game_mode.map.tileHeight * 20
        info_path = path.join(IMAGE_DIR, INFO_NAME)
        info_url = INFO_URL
        game_info["assets"].append(create_asset_init_data("info", 306, 480, info_path, info_url))
        logo_path = path.join(IMAGE_DIR, LOGO)
        logo_url = LOGO_URL
        game_info["assets"].append(create_asset_init_data("logo", 40, 40, logo_path, logo_url))

        for car in self.game_mode.car_info:
            file_path = path.join(IMAGE_DIR, CARS_NAME[car["id"]])
            url = CARS_URL[car["id"]]
            car_init_info = create_asset_init_data("car_0" + str(car["id"]+1), 50, 50, file_path, url)
            game_info["assets"].append(car_init_info)
        return game_info

    @check_game_progress
    def get_scene_progress_data(self) -> dict:
        """
        Get the position of game objects for drawing on the web
        """
        game_progress = {
            "background": [],
            "object_list": [],
            "toggle": [],
            "foreground": [],
            "user_info": [],
            "game_sys_info": {"view_center_coordinate":[250 - self.game_mode.car_info[0]["center"][0], 240 - self.game_mode.car_info[0]["center"][1]]}
        }

        # wall
        for wall in self.game_mode.walls:
            vertices = [(wall.body.transform * v) for v in wall.box.shape.vertices]
            vertices = [self.game_mode.trnsfer_box2d_to_pygame(v) for v in vertices]
            game_progress["object_list"].append(create_polygon_view_data("wall", vertices, "#ffffff"))
        # end point
        game_progress["object_list"].append(create_image_view_data("logo", self.game_mode.end_point.rect.x, self.game_mode.end_point.rect.y,
                             50, 50))
        # rect
        game_progress["toggle"].append(create_rect_view_data("rect", 0, 0, TILE_LEFTTOP[0], HEIGHT, "#000000"))
        game_progress["toggle"].append(create_rect_view_data("rect", 0, 0, WIDTH, TILE_LEFTTOP[1], "#000000"))
        game_progress["toggle"].append(create_rect_view_data("rect", TILE_LEFTTOP[0] + TILE_WIDTH, 0,
                                                           WIDTH - TILE_LEFTTOP[0] - TILE_WIDTH, HEIGHT, "#000000"))
        game_progress["toggle"].append(create_rect_view_data("rect", 0, TILE_LEFTTOP[1] + TILE_HEIGHT,
                                                           WIDTH, HEIGHT, "#000000"))
        p = self.game_mode.trnsfer_box2d_to_pygame((0,0))
        game_progress["object_list"].append(create_rect_view_data("rect", p[0], p[1], 10, 10, "#356425"))
        # info
        game_progress["toggle"].append(create_image_view_data("info", 507, 20, 306, 480))
        # car
        for car in self.game_mode.car_info:
            game_progress["object_list"].append(
                create_image_view_data("car_0"+str(car["id"]+1), car["topleft"][0], car["topleft"][1], 50, 40, car["angle"])
            )

        # text
        for car in self.game_mode.car_info:
            if car["id"] % 2 == 0:
                x = 600
            else:
                x = 730

            if car["status"]:
                game_progress["toggle"].append(
                    create_text_view_data("L:" + str(car["l_sensor_value"]["distance"]) + "cm", x, 178 + 20 + 94 * (car["id"] // 2), "#FFFF00",
                                   "15px Arial"))
                game_progress["toggle"].append(
                    create_text_view_data("F:" + str(car["f_sensor_value"]["distance"]) + "cm", x, 178 + 40 + 94 * (car["id"] // 2), "#FF0000",
                                   "15px Arial"))
                game_progress["toggle"].append(
                    create_text_view_data("R:" + str(car["r_sensor_value"]["distance"]) + "cm", x, 178 + 60 + 94 * (car["id"] // 2), "#21A1F1",
                                   "15px Arial"))
                game_progress["object_list"].append(create_line_view_data("l_sensor", car["center"][0], car["center"][1],
                                                                    self.trnsfer_box2d_to_pygame(car["l_sensor_value"]["coordinate"])[0],
                                                                    self.trnsfer_box2d_to_pygame(car["l_sensor_value"]["coordinate"])[1],
                                                                    "#FFFF00", 5))

                game_progress["object_list"].append(create_line_view_data("l_top_sensor", car["center"][0], car["center"][1],
                                                                    self.trnsfer_box2d_to_pygame(car["l_t_sensor_value"]["coordinate"])[0],
                                                                    self.trnsfer_box2d_to_pygame(car["l_t_sensor_value"]["coordinate"])[1],
                                                                    "#FFFF00", 5))

                game_progress["object_list"].append(create_line_view_data("r_top_sensor", car["center"][0], car["center"][1],
                                                                    self.trnsfer_box2d_to_pygame(car["r_t_sensor_value"]["coordinate"])[0],
                                                                    self.trnsfer_box2d_to_pygame(car["r_t_sensor_value"]["coordinate"])[1],
                                                                    "#21A1F1", 5))
                game_progress["object_list"].append(create_line_view_data("r_sensor", car["center"][0], car["center"][1],
                                                                    self.trnsfer_box2d_to_pygame(car["r_sensor_value"]["coordinate"])[0],
                                                                    self.trnsfer_box2d_to_pygame(car["r_sensor_value"]["coordinate"])[1],
                                                                    "#21A1F1", 5))
                game_progress["object_list"].append(create_line_view_data("f_sensor", car["center"][0], car["center"][1],
                                                                    self.trnsfer_box2d_to_pygame(car["f_sensor_value"]["coordinate"])[0],
                                                                    self.trnsfer_box2d_to_pygame(car["f_sensor_value"]["coordinate"])[1],
                                                                    "#FF0000", 5))
            else:
                game_progress["toggle"].append(create_text_view_data(str(car["end_frame"]) + "frame",
                                                                  x, 178 + 40 + 94 * (car["id"] // 2), "#FFFFFF", "15px Arial"))

        return game_progress

    @check_game_result
    def get_game_result(self):
        """
        Get the game result for the web
        """
        scene_info = self.get_scene_info
        result = self.game_mode.result
        rank = []
        for ranking in self.game_mode.ranked_user:
            same_rank = []
            for user in ranking:
                same_rank.append({"player":str(user.car_no+1)+"P",
                                  "frame_used":user.end_frame} )
            rank.append(same_rank)

        return {"frame_used": scene_info["frame"],
                "state":self.game_result_state,
                "attachment": rank,
                }

        pass

    def get_keyboard_command(self):
        """
        Get the command according to the pressed keys
        """
        key_pressed_list = pygame.key.get_pressed()
        cmd_1P = [{"left_PWM": 0, "right_PWM": 0}]
        cmd_2P = [{"left_PWM": 0, "right_PWM": 0}]

        if key_pressed_list[pygame.K_UP]:
            cmd_1P[0]["left_PWM"] = 100
            cmd_1P[0]["right_PWM"] = 100
        if key_pressed_list[pygame.K_DOWN]:
            cmd_1P[0]["left_PWM"] = -100
            cmd_1P[0]["right_PWM"] = -100
        if key_pressed_list[pygame.K_LEFT]:
            cmd_1P[0]["right_PWM"] += 100
        if key_pressed_list[pygame.K_RIGHT]:
            cmd_1P[0]["left_PWM"] += 100

        if key_pressed_list[pygame.K_w]:
            cmd_2P[0]["left_PWM"] = 100
            cmd_2P[0]["right_PWM"] = 100
        if key_pressed_list[pygame.K_s]:
            cmd_2P[0]["left_PWM"] = -100
            cmd_2P[0]["right_PWM"] = -100
        if key_pressed_list[pygame.K_a]:
            cmd_2P[0]["right_PWM"] += 100
        if key_pressed_list[pygame.K_d]:
            cmd_2P[0]["left_PWM"] += 100

        return {"ml_1P": cmd_1P,
                "ml_2P": cmd_2P}

    def trnsfer_box2d_to_pygame(self, coordinate):
        '''
        :param coordinate: vertice of body of box2d object
        :return: center of pygame rect
        '''
        return ((coordinate[0] - self.game_mode.pygame_point[0]) * PPM, (self.game_mode.pygame_point[1] - coordinate[1]) * PPM)