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
echo "behavior_ecoute et pocketSphinx"
xterm -e "roslaunch pocketsphinx behavior_ecoute.launch" &
echo "behavior_verifie_batterue"
xterm -e "rosrun spike behavior_verifie_batterie.py" &
echo "behavior_joue_son"
xterm -e "rosrun spike behavior_joue_son.py" &
#echo "behavior_saisie_son_ambiant"
#xterm -e "rosrun spike behavior_saisie_son_ambiant.py" &
echo "behavior_idle"
xterm -e "rosrun spike behavior_idle.py" &
echo "behavior_detecte_ambiance_classe_snn"
#xterm -e "roslaunch spike behavior_detecte_ambiance_classe_SNN.launch" &
#echo "behavior_detecte_son528Hz_snn"
#xterm -e "roslaunch spike behavior_detecte_son528Hz_SNN.launch" &
echo "behavior_selection"
xterm -e "rosrun spike behavior_selection.py" &
#export DISPLAY=':0'
echo "behavior_humeur"
xterm -e "rosrun spike behavior_humeur.py" &

echo "SPIKE LAUNCHED!"
