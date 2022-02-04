import os
from shutil import copy

img_dir = os.path.join(os.getcwd(), 'Images')
imgs = [f for f in os.listdir(img_dir) if f.split('.')[-1] == 'jpg']
imgs.sort()

results_dir = os.path.join(os.getcwd(), 'Results')
run_count = 1
for i in range(0, len(imgs)-1, 2):
    run_img_0 = os.path.join(img_dir, imgs[i])
    run_img_90 = os.path.join(img_dir, imgs[i+1])
    
    img_name = os.path.basename(run_img_0).split('.')[0][:-6]
    
    old_out_dir = img_name + '_Old'
    old_out_dir = os.path.join(results_dir, old_out_dir)
    if os.path.exists(old_out_dir):
        pass
    else:
        os.mkdir(old_out_dir)
        copy(run_img_0, old_out_dir)
        copy(run_img_90, old_out_dir)
        
        os.chdir(old_out_dir)
        
        old_outputs = os.popen('bash /home/samuel/Desktop/Projects/pin_align-master-bash/pin_align_fmx.sh ' + os.path.basename(run_img_0) + ' ' + os.path.basename(run_img_90)).readlines()
        
        old_config = open('run_output.txt', 'w')
        old_config.writelines(old_outputs)
        
        old_config.close()
        os.chdir(img_dir)
     
    # New config file generated from the auto config GUI
    new_out_dir = img_name + '_New'
    new_out_dir = os.path.join(results_dir, new_out_dir)
    if os.path.exists(new_out_dir):
        pass
    else:
        os.mkdir(new_out_dir)
        copy(run_img_0, new_out_dir)
        copy(run_img_90, new_out_dir)
        
        os.chdir(new_out_dir)
        
        new_outputs = os.popen('bash /home/samuel/Desktop/Projects/pin_align-master/FMX/pin_align_fmx.sh ' + os.path.basename(run_img_0) + ' ' + os.path.basename(run_img_90)).readlines()
        
        new_config = open('run_output.txt', 'w')
        new_config.writelines(new_outputs)
        
        new_config.close()
        os.chdir(img_dir) 
    # if run_count == 100:
    #     break
    # else:
    #     run_count+=1