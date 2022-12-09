import json 
import os

for subdir, dirs, files in os.walk('results'):
    for file in files:
        if file == 'gaze.txt':
            print(os.path.join(subdir,file))


            with open(os.path.join(subdir,'gaze.txt')) as f:
                data = f.read()
            data_points = data.split('\n')
            tobii_data = []
            conversion_count = 0
            error_count = 0
            for data_point in data_points:
                try:
                    orig_json = json.loads(data_point.replace("'","\"").replace('(','[').replace(')',']'))
                    # orig_json = json.loads(data_point.replace("'","\"").replace('(','[').replace(')',']').replace("nan",'"nan"'))
                    tobii_json = {}
                    tobii_json["Timestamp"] = orig_json["system_time_stamp"]
                    tobii_json["LeftEye"] = {}
                    tobii_json['LeftEye']["Validity"]="Valid"
                    tobii_json['LeftEye']["GazePoint2D"]={}
                    tobii_json['LeftEye']["GazePoint2D"]["X"] = orig_json["left_gaze_point_on_display_area"][0]
                    tobii_json['LeftEye']["GazePoint2D"]["Y"] = orig_json["left_gaze_point_on_display_area"][1]
                    tobii_json['LeftEye']["GazePoint3D"]={}
                    tobii_json['LeftEye']["GazePoint3D"]["X"] = orig_json["left_gaze_point_in_user_coordinate_system"][0]
                    tobii_json['LeftEye']["GazePoint3D"]["Y"] = orig_json["left_gaze_point_in_user_coordinate_system"][1]
                    tobii_json['LeftEye']["GazePoint3D"]["Z"] = orig_json["left_gaze_point_in_user_coordinate_system"][2]
                    tobii_json['LeftEye']["EyePosition3D"] = {}
                    tobii_json['LeftEye']["EyePosition3D"]["X"] = orig_json["left_gaze_origin_in_user_coordinate_system"][0]
                    tobii_json['LeftEye']["EyePosition3D"]["Y"] = orig_json["left_gaze_origin_in_user_coordinate_system"][1]
                    tobii_json['LeftEye']["EyePosition3D"]["Z"] = orig_json["left_gaze_origin_in_user_coordinate_system"][2]
                    tobii_json['LeftEye']['PupilDiameter'] = orig_json["left_pupil_diameter"]

                    tobii_json["RightEye"] = {}
                    tobii_json['RightEye']["Validity"]="Valid"
                    tobii_json['RightEye']["GazePoint2D"]={}
                    tobii_json['RightEye']["GazePoint2D"]["X"] = orig_json["right_gaze_point_on_display_area"][0]
                    tobii_json['RightEye']["GazePoint2D"]["Y"] = orig_json["right_gaze_point_on_display_area"][1]
                    tobii_json['RightEye']["GazePoint3D"]={}
                    tobii_json['RightEye']["GazePoint3D"]["X"] = orig_json["right_gaze_point_in_user_coordinate_system"][0]
                    tobii_json['RightEye']["GazePoint3D"]["Y"] = orig_json["right_gaze_point_in_user_coordinate_system"][1]
                    tobii_json['RightEye']["GazePoint3D"]["Z"] = orig_json["right_gaze_point_in_user_coordinate_system"][2]
                    tobii_json['RightEye']["EyePosition3D"] = {}
                    tobii_json['RightEye']["EyePosition3D"]["X"] = orig_json["right_gaze_origin_in_user_coordinate_system"][0]
                    tobii_json['RightEye']["EyePosition3D"]["Y"] = orig_json["right_gaze_origin_in_user_coordinate_system"][1]
                    tobii_json['RightEye']["EyePosition3D"]["Z"] = orig_json["right_gaze_origin_in_user_coordinate_system"][2]
                    tobii_json['RightEye']['PupilDiameter'] = orig_json["right_pupil_diameter"]

                    tobii_data.append(tobii_json)
                    conversion_count += 1
                except:
                    # print(data_point)
                    error_count += 1
                    

                
            print(conversion_count, error_count)
            with open(os.path.join(subdir,'gaze_converted.json'), 'w+') as outfile:
                json.dump(tobii_data, outfile)