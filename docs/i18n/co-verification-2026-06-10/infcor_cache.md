# Cache de vérification INFCOR (ADECEC — Banca di dati di a lingua corsa)

Source: `https://adecec.net/infcor/try/swift.php?langue=mot_corse&mot=<mot>&part=first`
Chaque entrée = id `unique` INFCOR (stable, citable) + formes attestées + glose FR.

Format: `mot_co | INFCOR id | formes attestées | glose FR | verdict`
verdict: OK (attesté, sens conforme) · SENS? (attesté, sens à arbitrer) · CORR (forme à corriger) · ABS (absent)

| mot CO (modèle) | INFCOR id | formes attestées | glose FR INFCOR | verdict |
|---|---|---|---|---|
| palesà | 32510 | palisà / palesà | avouer, divulguer, dévoiler, manifester | SENS? (révéler≈dévoiler ok; arbitrer vs svelà/rivelà — tagline) |
| invisibile | 24474 | invisibile / imbisibile | invisible | OK |
| attrezzu | 5190 | attracciu/attrezzu… | instrument, outil | OK |
| cuncipitu | 12221 | cuncepitu / cuncipitu | conçu | OK |
| citatinu/citatina | 53963 | citadinu / citatinu | citadin (urbain) | SENS? faux-sens possible pour « citoyen » — FLAG |
| esplurazione | 16581 | esplurazione / splurazione | exploration | OK |
| cartugrafia | 9066 | cartografia/cartugrafia | cartographie | OK |
| scentifica | 42211 | scientificu/scentificu | scientifique | OK |
| territoriu | 48949 | territoriu | territoire | OK |
| cuntenutu | 12906 | cuntenutu/contenutu | contenu | OK |
| benvenuti | 6526 | benvenutu/benvinutu | bienvenue | OK |
| rimpiazza | 39205 | rimpiazzà | remplacer | OK |
| prufessiunale | 36718 | prufessiunale/professionale | professionnel | OK |
| metodulugia | 28060 | metodulugia/metudulugia | méthodologie | OK |
| accolta | 839 | accolta | accueil | OK |
| fonti | 18021 | fonte/fonti | source, documentation | OK |
| elettromagnetica | 15612 | elettromagneticu | électromagnétique | OK |
| campu | 54907 | campu | champ | OK |
| cuntribuisce | 12821 | cuntribuì/cuntribuisce | contribuer | OK |
| privata | 36306 | privatu/privata | privé; particulier | OK |
| spartite | 45664/45282 | spartì→spartutu/spartimentu | partager | OK (impératif 2pl) |
| ligata | 25541 | ligatu/ligata | lié, attaché | OK |
| verificata | 51513 | verificatu | vérifié | OK |
| verificazione | 51508 | verifica/verificazione | vérification | OK |
| publicata | 37088 | publicatu | publié | OK |
| sensazione | 43235 | sensazione | sensation | OK (≈ressenti) |
| cuntestu | 12917 | cuntestu/contestu | contexte | OK |
| mandà | 26627 | mandà | mander, envoyer | OK |
| particulare | 32904 | particulare | particulier; détail | OK |
| carta | 9044 | carta/cartula | papier, carte | OK |
| puntu | 37341 | puntu | point; but | OK |
| stratu/strati | 46893 | stratu | couche, strate | OK |
| chjode | 707 | acchjude/chjode/chjude | enfermer, renfermer, inclure | SENS? (chjude=fermer usuel; glose accentue « enfermer ») |
| annullà | 3272 | annullà | annuler | OK |
| aviò | 5581 | avviò/aviò | avion | OK |
| telefonu | 48687 | telefunu/telefonu | téléphone | OK |
| merria/merrie | — | ABSENT (merra=houe; mirrachjolu=petit maire) | — | **FLAG** mairie non attesté (cf. casa cumuna / cumuna) |
| acciaghju | 748 | acciaghju/acciaiu | acier | OK |
| intonacu | — | ABSENT | — | **FLAG** enduit non attesté (italianisme ?) |
| ghjessu | 19235 | ghjessu | gypse, plâtre | OK |
| bluchettu | — | ABSENT | — | **FLAG** parpaing non attesté |
| geulugia | 19035 | geolugia/geulugia | géologie | OK |
| idrugrafia | 20241 | idrografia/idrugrafia | hydrographie | OK |
| anumalia/anumalie | 3447 | anumalia/anomalia | anomalie | OK |
| antenna/antenne | 3325 | antenna | antenne | OK |
| radiazione | 37564 | radiazione | radiation | OK |
| frequenza | 18141 | frequenza/friquenza | fréquence | OK |
| granitu | 19747 | granitu | granit | OK |
| schistu | 42275 | scistu/schistu | schiste | OK |
| calcariu | 7920 | calcariu/calcare | calcaire | OK |
| faglia/faglie | — | ABSENT | — | **FLAG** faille (géol.) non attesté (italianisme ?) |
| cavità | 9503 | cavità | cavité | OK |
| furesta/fureste | 18577 | furesta/foresta | forêt | OK |
| riduce | 38856 | riduce | réduire | OK |
| colonna | 11948 | culonna/colonna | colonne | OK |
| filtru | 17545 | filtru | filtre | OK |
| duminiu | 15452 | duminiu/dominiu | domaine | OK |
| modu | 28927 | modu | mode, façon | OK |
| modulu | 28775 | modulu | module | OK |
| mudulazione | 29326 | mudulazione | modulation | OK |
| mudellu | 29238 | mudellu/modellu | modèle | OK |
| espertu/esperti | 16367 | espertu/spertu | expert | OK |
| vista | 51996 | vista | vue | OK |
| indice | 22460 | indice | index, indice | OK |
| statistiche | 46410 | statistica | statistique | OK |
| cundizione | 12508 | cundizione/condizione | condition | OK |
| terrenu | 48934 | terrenu/tarrenu | terrain | OK |
| numeru | 30891 | numeru/numaru | numéro, nombre | OK |
| cliccà/cliccate | — | clicca=clique; cricca=loquet (PAS le verbe) | — | **FLAG** « cliquer » (informatique) non attesté |
| piazzà/piazzatu | 34550 | piazza/piazzatu | placé, mis en place | OK |
| aduprà | 21539 | adoprà/aduprà | employer, utiliser | OK |
| adupratu | 1364 | adupratu | utilisé | OK |
| piantà | 34475 | piantà/pientà | planter; arrêter | OK (=arrêter) |
| arregistrà | 4360 | arregistrà/registrà | enregistrer | OK |
| arregistramentu | 38433 | registramentu/arregistramentu | enregistrement | OK |
| principià | (recheck) | — | démarrer/commencer | RECHECK |
| generà | (recheck) | — | générer | RECHECK |
| espurtà | 16611 | espurtà/esportà | exporter | OK |
| esportu | 16614 | espurtazione/esportu | export | OK |
| circà | 10686 | circà/cercà | chercher, rechercher | OK |
| capisce | 8508 | capì/capisce | comprendre | OK |
| accede | 622 | accede | accéder | OK |
| valore | 51238 | valore | valeur | OK |
| unità | 50939 | unità | unité | OK |
| strumentu | 23894 | strumentu/istrumentu | instrument | OK |
| principià | 36568 | principià/principiatu | commencer, débuter | OK (=démarrer) |
| generà | — | ABSENT (general* oui, mais pas le verbe) | — | **FLAG** « générer » non attesté (cf. creà/pruduce) |
| magnetometru | 26263 | magnetometru | magnétomètre | OK |
| orientazione | 31847 | orientazione | orientation | OK |
| media | 27633 | media/mediana | moyenne | OK |
| mediana | 27636 | mediana | médiane | OK |
| campione/campioni | 8223 | campione | échantillon, champion | OK |
| raportu | 38162 | raportu | rapport | OK |
| gradiente | — | ABSENT | — | **FLAG** « gradient » non attesté |
| interpretazione | 24013 | interpretazione | interprétation | OK |
| sistemu | 44452 | sistemu/sistema | système | OK |
| pusizione | 37537 | pusizione/posizione | position | OK |
| finestra | 17730 | finestra | fenêtre | OK |
| sulare | 47541 | sulare/solare | solaire | OK |
| ventu | 51457 | ventu | vent | OK |
| flussu | 17975 | flussu | flux | OK |
| densità | 13774 | densità | densité | OK |
| currezzione | 13320 | currezzione/correzzione | correction | OK |
| acquisizione | — | ABSENT | — | **FLAG** « acquisition » non attesté (cf. acquistu) |
| timpurale | (49.) | tempuralescu/timpuralescu = orageux (adj) | orage/orageux | SENS? noun « orage » non confirmé direct — FLAG léger |
| atmosfericu | 5057 | atmusfericu/atmosfericu | atmosphérique | OK |
| prutone/prutoni | — | ABSENT | — | **FLAG** « proton » non attesté |
| paragone | 32672 | paragone/paragonu | comparaison, parallèle | OK |
| paragunevule | 32962 | paragunevule | comparable | OK |
