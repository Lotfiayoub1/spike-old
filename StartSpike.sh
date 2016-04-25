# Lancement de SPIKE
# Par JS.Dessureault
#
# Notes: 
# Parametres de xterm
#	-e "ligne de commande avec parametres"
# 	& Execute en tache de fond
#	-hold  : ne ferme pas la fenetre apres execution

cd ~/catkin_ws/
echo "Killing all previous processes..."
pkill roscore 
pkill python  
echo "LAUNCHING SPIKE..."
echo "roscore..."
xterm roscore &
sleep 5
echo "sound_play..."
xterm -e "roslaunch sound_play soundplay_node.launch" &
sleep 3
echo "pocketSphinx"
xterm -e "roslaunch reconnaissanceVoix pocket_sphinx.py" &
sleep 3
echo "freenect"
xterm -e "roslaunch freenect_launch freenect.launch" &
sleep 3
echo "behavior_parle"
xterm -e "rosrun spike behavior_parle.py" &
sleep 2
echo "behavior_joue_son"
xterm -e "rosrun spike behavior_joue_son.py" &
sleep 2
echo "behavior_ecoute"
xterm -e "rosrun spike behavior_ecoute.py" &
sleep 2
echo "behavior_chatbot_aiml"
xterm -e "rosrun spike behavior_chatbot_aiml.py" &
sleep 2
echo "behavior_humeur"
xterm -e "rosrun spike behavior_humeur.py" &
sleep 2
echo "behavior_idle"
xterm -e "rosrun spike behavior_idle.py" &
sleep 2
#echo "behavior_deplacement"
#xterm -e "rosrun spike behavior_deplacement.py" &
#sleep 2
echo "behavior_attention"
xterm -e "rosrun spike behavior_attention.py" &
sleep 2
echo "SPIKE LAUNCHED!"
