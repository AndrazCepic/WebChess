<!DOCTYPE html>
<html>
<head>
    <title>Spletni Šah</title>
    <link rel="stylesheet" href="/static/main.css">
</head>
<body>
    <div id="new_game">
        <form action="new_game" method="POST">
                <input id="new_game_button" type="submit" name="new_game" value="Nova Igra">
        </form>
    </div>
    
    <div class="info">
        % if prom_w or prom_b:
            <p>Izberi promocijsko figuro!</p>
        % else:
            % if igra.stanje_igre == igra.STANJA["beli_pot"]:
                <p>Bel je na potezi!</p>
            % elif igra.stanje_igre == igra.STANJA["crni_pot"]:
                <p>Črn je na potezi!</p>
            % elif igra.stanje_igre == igra.STANJA["mat_beli"]:
                <p>Bel je zmagal!</p>
            % elif igra.stanje_igre == igra.STANJA["mat_crni"]:
                <p>Črn je zmagal!</p>
            % elif igra.stanje_igre == igra.STANJA["pat"]:
                <p>Igra je končana neodločeno!</p>
            % end
        % end
    </div>

    % if prom_w:
    <form action="promotion" method="POST">
    <div class="promotion">
        <div class="piece">
            <input class="input" type="submit" name="prom_fig" value="q">
            <img src="/static/w_q.png"></img>
        </div>
        <div class="piece">
            <input class="input" type="submit" name="prom_fig" value="r">
            <img src="/static/w_r.png"></img>
        </div>
        <div class="piece">
            <input class="input" type="submit" name="prom_fig" value="b">
            <img src="/static/w_b.png"></img>
        </div>
    </div>
    </form>
    % else:
    <div class="promotion_bl"></div>
    % end
    <form action="/board_input" method="POST">
        <div class="igra">
            <div class="captured_pieces_w">
                    <%
                    for fig in igra.zajete_fig_beli:
                        fig_s = igra.fig_v_str(fig)
                    %>
                        <div class="piece">
                            <img src="/static/{{fig_s}}.png"></img>
                        </div>
                    % end
            </div>
            <div class="board">
                <%  for y_i in range(8): 
                        for x in range(8):
                            y = 7 - y_i
                            barva = ""
                            if ((x % 2 == 0 and y % 2 == 0) or
                                (x % 2 != 0 and y % 2 != 0)):
                                barva = "square_b"
                            else:
                                barva = "square_w"
                            end

                            fig = igra.figura_na_poz(x, y)
                %>
                    <div class="{{barva}}">
                            % if not prom_w and not prom_b:
                                <input class="input" type="submit" name="click" value="{{x}}{{y}}">
                            % end
                            % if fig != None:
                                <img src="/static/{{fig}}.png"></img>
                            % end
                    </div>
                % end
                % end
            </div>
            <div class="captured_pieces_b">
                    <%
                    for fig in igra.zajete_fig_crni:
                        fig_s = igra.fig_v_str(fig)
                    %>
                        <div class="piece">
                            <img src="/static/{{fig_s}}.png"></img>
                        </div>
                    % end
            </div>
        </div>
    </form>
    % if prom_b:
    <form action="promotion" method="POST">
    <div class="promotion">
        <div class="piece">
            <input class="input" type="submit" name="prom_fig" value="q">
            <img src="/static/b_q.png"></img>
        </div>
        <div class="piece">
            <input class="input" type="submit" name="prom_fig" value="r">
            <img src="/static/b_r.png"></img>
        </div>
        <div class="piece">
            <input class="input" type="submit" name="prom_fig" value="b">
            <img src="/static/b_b.png"></img>
        </div>
    </div>
    </form>
    % else:
    <div class="promotion_bl"></div>
    % end
</body>
</html>