from riotwatcher import LolWatcher, ApiError
from time import sleep
import pandas as pd
import numpy as np

summoners_list = {
"Stepz" : "step z z",
"Ceviche0709" : "Ceviche Ans",
"DeusCloud3" : "Maniveela",
"PapiSosa" : "NO SOY CACHETON",
"Relic" : "xXElMasCapitoXx",
"Amauryn29" : "Silver Destroyer",
"Joker Was Here" : "Pykent was here",
"Masorco" : "secret TTQ jg",
"Mechs" : "ł Eros ł",
"MurilloSama" : "POCHO DIFF",
"ReinnLol" : "REDBULL ABUSER",
"Zenitzuuwu" : "TheKingVolibear",
"Lol Hugo Rock" : "TwTV lolHugrock",
"Lgsus" : "VA POR TI SOFI"
}
#"El Victorioso G" : "Taco sin Salsa",
#"Lukwer" : "LukiTuki",
#"Manzanoides" : "ASTROMANZANA99",
#"AnotherDeivid" : "Noxian Meow",
#"Bejjaniii" : "",
#"blurelle" : "Rapid 99",
#"CrystalMolly" : "Tacos de Molly",
#"Feng" : "TwitchTvFenglolz",
#"FRS Fiora" : "FRS Venus",
#"Mawuf" : "Fairers Tre",
#"Seranok" : "Séranok",
#"SoyRoola" : "",
#"Straightlol" : "",
#"Taaavo" : "",
#"Tio Steve" : "Estalladito Pa",
#"Ubaman" : "Duko Lover",
#"Zeith" : "Zeithking",
#"El Hola Silver" : "xAGradamentePRO",
#"Kaiser Wolf" : "ChivasLover8",
#"Marvin Sixx" : "Va por ti Ganks",
#"Mercy Plays" : "Tilin GAP",
#"Misrra" : "",
#"qShiroo" : "RaccAttack",
#"Crecrexd" : "OTPS XD",
#"Brayayin" : "Brayaqueen",
#"Fallen IV" : "TTG Kevorrea IV",
#"Jim Rising" : "Jim Rising",
#"Kameoyo" : "",
#"MarioMe" : "",
#"Miquelonsh" : "Baguette Diff",
#"Qwermiguel" : "Príncipe Inca",
#"Meethodz" : "lose mind win lp",

players = []
summoners_names = []
summoners_elo = []
summoners_games = []
current_win_ratio = []
summoner_division = []
summoner_rank = []
true_elo = []
total_wins = []
total_losses = []
debugged_tier = ["MASTER", "GRANDMASTER","CHALLENGER"]
summoner_upgrade_rank = []

for player in summoners_list.keys():
    players.append(player)

for summoner_name in summoners_list.values():

    api_key = "RGAPI-cfb4e3d4-b3f3-4a3c-b614-bdae4435dc18"
    watcher = LolWatcher(api_key)
    my_region = 'LA1'
    me = watcher.summoner.by_name(my_region, summoner_name)
    sleep(15)

    all_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
    if all_ranked_stats[0]["queueType"] == "RANKED_SOLO_5x5":
        valor = '1'
    else:
        valor = '2'

    practica = np.array(all_ranked_stats)[int(valor)-1]
    soloq_ranked_stats = practica
    
    currentTier = soloq_ranked_stats['tier']
    currentRank = soloq_ranked_stats['rank']
    currentLeaguePoints = soloq_ranked_stats['leaguePoints']
    currentWins = soloq_ranked_stats['wins']
    currentLossses = soloq_ranked_stats['losses']
    
    summoners_names.append(summoner_name)
    summoners_elo.append(currentLeaguePoints)
    summoners_games.append(currentWins + currentLossses)
    win_ratio = str(round(100*(currentWins/(currentLossses + currentWins)))) + ' %'
    current_win_ratio.append(win_ratio)
    summoner_division.append(currentTier)
    summoner_rank.append(currentRank)
    rank_calculator = int(((((currentRank.replace("IV", "1")).replace("III", "2")).replace("II", "3")).replace("I", "4")))
    total_wins.append(currentWins)
    total_losses.append(currentLossses)
    # auxiliarRank = ()
    # if currentRank =="I":
    #     auxiliarRank.append("4")
    #     if currentRank == "II":
    #         auxiliarRank.append("3")
    #         if currentRank == "III":
    #             auxiliarRank.append("2")
    #             if currentRank == "IV":
    #                 auxiliarRank.append("1")
        
    
    elocalculator = int(((((((((currentTier.replace("IRON", "1")).replace("BRONZE", "2")).replace("SILVER", "3")).replace("GOLD", "4"))
            .replace("PLATINUM", "5").replace("DIAMOND", "6").replace("MASTER", "7").replace("GRAND MASTER", "7").replace("CHALLENGER", "7"))))))
    eloID = 1000*elocalculator + (int(rank_calculator))*100 + currentLeaguePoints
    true_elo.append(eloID)
    if currentTier in debugged_tier:
        summoner_upgrade_rank.append(currentTier)
    else:
        summoner_upgrade_rank.append(currentTier + ' ' + currentRank)



dict_data = {"Nombre de Jugador": players,'Nombre de Invocador' : summoners_names, 'EloID': true_elo, 
 'División' : summoner_division, 'Tier':summoner_rank, 'Liga Actual' : summoner_upgrade_rank,'Puntos de Liga' : summoners_elo, 
 'Partidas Jugadas' : summoners_games, 'Victorias': total_wins, 'Derrotas': total_losses, 'Win Ratio %' : current_win_ratio}

df = pd.DataFrame(dict_data)
by_elo = df.sort_values("EloID", ascending=False)
#html_elo = (by_elo.to_html())
by_elo2 = by_elo[['Nombre de Jugador','Nombre de Invocador', 'Liga Actual', 'Puntos de Liga', 'Partidas Jugadas', 'Victorias', 'Derrotas', 'Win Ratio %']]
by_elo = by_elo2.to_csv('DB.csv', index = False)
print(by_elo2)