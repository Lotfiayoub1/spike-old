# Lancement de SPIKE
# Par JS.Dessureault
#
# Notes: 
# Parametres de xterm
#	-e "ligne de commande avec parametres"
# 	& Execute en tache de fond
#	-hold  : ne ferme pas la fenetre apres execution

cd ~/catkin_ws/
echo "LAUNCHING SPIKE..."
echo "roscore..."
xterm roscore &
sleep 5
echo "behavior_chatbot_aiml"
xterm -e "rosrun spike behavior_chatbot_aiml.py" &
echo "sound_play..."
xterm -e "roslaunch sound_play soundplay_node.launch" &
sleep 10
echo "behavior_parle"
xterm -e "rosrun spike behavior_parle.py" &
#echo "freenect"
#xterm -e "roslaunch freenect_launch freenect.launch" &
echo "behavior_ecoute et pocketSphinx"
xterm -e "roslaunch pocketsphinx behavior_ecoute.launch" &
echo "behavior_joue_son"
xterm -e "rosrun spike behavior_joue_son.py" &
#echo "behavior_deplacement"
#xterm -e "rosrun spike behavior_deplacement.py" &
echo "behavior_idle"
xterm -e "rosrun spike behavior_idle.py" &
echo "behavior_attention"
xterm -e "rosrun spike behavior_attention.py" &
#export DISPLAY=':0'
echo "behavior_humeur"
xterm -e "rosrun spike behavior_humeur.py" &
echo "SPIKE LAUNCHED!"
