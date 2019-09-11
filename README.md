# WebChess
Preprosta aplikacija za igranje šaha, ki teče na bottle serverju.
Strežnik aplikacije zaženemo z app.py, ta pa je dosegljiv na localhost:8080.

Funkcionalnost aplikacije je igranje šaha z vnosom potez preko klikov z miško, kjer se upooštevajo le legalne poteze.
Vsaka poteza je vnešena, da uporabnik prvo klikne na figuro, ki jo želi premakniti, nato pa klikne na željeno destinacijo figure.

Možne nadgraditve:
1. Preprosta umetna inteligenca(Alpha-Beta pruning s preprosto evalvacijo figur)
2. PGN parsing za shranjevanje in nalaganje iger v engine
3. Timer za igre(npr. za blitz)