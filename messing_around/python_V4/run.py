from pearing_class_functions import Pear_Playlists
import time
from pearing_classes import Playlist_Base
#playlist_name_1 = 'Snowboarding Hype'
#playlist_name_2 = 'Snowboarding Chill'
playlist_name_1 = 'Chill Alt Rock'
playlist_name_2 = 'tmp2'

access_token = 'Bearer BQCh2_UhSf4xNnKS53RdCrPzgdyYcHw9GLVJcKTvQRu0ULGkT6viX_gP4ogM3FDfmyBf0betTrD-qUWwNHU_wLQksAgI11OIRHpSqULErDLVxDah6o9uhmgLy4goHBWPUu_z1SS8RLRuMr6odGD_jK0dRj2pIOljoJDfDCfJlL4OSeUbl_aP28G4Vt6Bx8qzakH-ACTKXjoFFU60Bti06Lgts5lXy57I7fXHT_SQtbgYKaHnt2fp7y1Lv_TrCjKWo1eoXw'
user_id = '22r6slwbns4u7hkhn3hjhjhyi'


start_time = time.time()

p1_base = Playlist_Base(playlist_name = playlist_name_1, user_id = user_id, access_token = access_token)

#Pear_Playlists(playlist_name_1, playlist_name_2, access_token, user_id)

print('took this long: ', time.time() - start_time)