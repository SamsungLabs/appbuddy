# AppBuddy: Learning to Accomplish Tasks in Mobile Apps via Reinforcement Learning
Human beings, even small children, quickly become adept at figuring out how to use applications on their mobile devices. Learning to use a new app is often achieved via trial-and-error, accelerated by transfer of knowledge from past experiences with like apps. The prospect of building a smarter smartphone --- one that can learn how to achieve tasks using mobile apps --- is tantalizing. In this paper we explore the use of Reinforcement Learning (RL) with the goal of advancing this aspiration. We introduce AppBuddy, an RL-based framework for learning to accomplish tasks in mobile apps. RL agents are provided with states derived from the underlying representation of on-screen elements, and rewards that are based on progress made in the task. Agents can interact with screen elements by tapping or typing. Our experimental results, over a number of mobile apps, show that RL agents can learn to accomplish multi-step tasks, as well as achieve modest generalization across different apps. We develop a platform which addresses several engineering challenges to enable an effective RL training environment. The platform includes a suite of mobile apps and benchmark tasks that supports a diversity of RL research in the mobile app setting. A video demonstration of the system is available here: https://youtu.be/UUP29BGH1ug.

Paper (including technical appendix): https://arxiv.org/abs/2106.00133 

If you use AppBuddy in your research, please cite our paper using the following BibTeX:

```
@inproceedings{shvoEtAl2021appbuddy,
  title={AppBuddy: Learning to Accomplish Tasks in Mobile Apps via Reinforcement Learning},
  author={Maayan Shvo and
               Zhiming Hu and
               Rodrigo Toro Icarte and
               Iqbal Mohomed and
               Allan D. Jepson and
               Sheila A. McIlraith},
  booktitle={Canadian Conference on Artificial Intelligence},
  year={2021}
}
```

## Prerequisites
Create a conda environment with prerequisite packages
```
conda create --name <env> --file req_conda.txt
```
then run
```
conda activate appbuddy
```

Install adb
```
sudo apt-get install android-tools-adb android-tools-fastboot
```

Initialize the adb server and ensure that there is a device runnning

```
adb devices
```

## Launch emulators

The script is start_emulators.sh located in the scripts folder. The number of emulators launched by the script can be changed by modifying the var variable. It is 3 by default.
```
sh start_emulators.sh
```
The script uses the following [repository](https://github.com/budtmo/docker-android) to create an individual docker container for each emulator. KVM is required so try installing it using

```
sudo yum install qemu-kvm
```
or the equivalent for your Linux distribution. After running the script, use
```
adb devices
```
to check whether the emulators have been properly initialized

## Start Bert Services
Clone this [repository](https://github.com/hanxiao/bert-as-service) and follow the installation instructions. From the same repository, download and extract the bert model (uncased_L-12_H-768_A-12.zip). After that, Run the following command to start the bert service. 

```
nohup bert-serving-start -model_dir uncased_L-12_H-768_A-12 -num_worker=20 -port 5000 -port_out 5005 &
```

## How to run the code - OpenAI baselines

Install baselines
```
cd baselines
```
Then run
```
pip install -e .
```
Then run
```
cd ../android_gym
```
and run

```
pip install -e .
```
and then 
```
cd ..
```
Then download the F-Droid apps' APKs
```
wget https://f-droid.org/repo/org.openintents.shopping_100221.apk
wget https://f-droid.org/repo/com.nishantboro.splititeasy_1.apk
wget https://f-droid.org/repo/com.angrydoughnuts.android.alarmclock_15.apk
```
Install the F-Droid apps using the downloaded APKs (xxxxx should be replaced with the emulator port (e.g., 30001) which can be found when executing adb devices)
```
adb -s localhost:xxxxx install com.angrydoughnuts.android.alarmclock_15.apk
adb -s localhost:xxxxx install com.nishantboro.splititeasy_1.apk
adb -s localhost:xxxxx install org.openintents.shopping_100221.apk
```

To choose what task to run (settings or alarm) and the difficulty (easy, medium, or hard), uncomment the relevant lines in the config.yaml file and change the value of difficulty_level.

Finally, run the following to being training:

```
OPENAI_LOGDIR=$HOME/logs OPENAI_LOG_FORMAT=csv python3 -m baselines.run --alg=ppo2 --env=Android-v0 --network=mlp --num_timesteps=4e6 --log_interval=1
```
## Train the agent on a new app

To train an agent on a new app (i.e., not one of the included apps), we must implement two app-specific functions: reset and get_reward.

Let's say you have an app called FooApp. To experiment with this app, you need to write a function that resets the app. For inspiration, take a look at the restart_settings function in settings_app.py. There, adb commands are issued to clear the app's data and to reopen the app since the clear command causes the app to terminate.

You will also need to implement a get_reward_for_current_state function that, given the current state of the emulator, returns a numerical reward as well as whether or not the episode is done (in case the task has been achieved). Once again, we can look at settings_app.py for inspiration. The function get_reward_for_current_state accepts as input the state of the emulator (i.e., the parsed view hierarchy comprising a list of UI elements) and returns the value of the reward as well as whether or not the episode is done. To make this more concerete, let's take a look at the easy task in the settings app. In this task, the agent gets a reward when it navigates to the Wi-Fi settings screen. To check this in the code, we check in line 65 in settings_app.py whether one of the UI elements has the value of 'Wi‑Fi preferences' in the obj_name attribute. Within the settings app, this uniquely identifies the screen and allows us to appropirately reward the agent for reaching it.

## Contributors
Maayan Shvo (maayanshvo@cs.toronto.edu) \
Zhiming Hu (zhiming.hu@samsung.com) \
Rodrigo	Toro Icarte (rntoro@cs.toronto.edu)\
Iqbal Mohomed (i.mohomed@samsung.com)\
Allan	Jepson (allan.jepson@samsung.com)\
Sheila A.	McIlraith	(sheila@cs.toronto.edu)
