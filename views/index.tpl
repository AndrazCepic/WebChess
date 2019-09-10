<!DOCTYPE html>
<html>
<head>
    <title>Spletni Šah</title>
    <link rel="stylesheet" href="/static/main.css">
</head>
<body>
    <div class="info">
        % if igra.stanje_igre == igra.STANJA["beli_pot"]:
            <p>Bel je na potezi</p>
        % elif igra.stanje_igre == igra.STANJA["crni_pot"]:
            <p>Črn je na potezi</p>
        % elif igra.stanje_igre == igra.STANJA["mat_beli"]:
            <p>Bel je zmagal!</p>
        % elif igra.stanje_igre == igra.STANJA["mat_crni"]:
            <p>Črn je zmagal!</p>
        % elif igra.stanje_igre == igra.STANJA["pat"]:
            <p>Igra je končana neodločeno!</p>
        % end
    </div>

    <form action="new_game" method="POST">
            <input id="new_game_button" type="submit" name="new_game" value="Nova Igra">
    </form>

    <form action="/board_input" method="POST">
        <div class="igra">
            <div class="captured_pieces">
                    <%
                    for fig in igra.zajete_fig_crni:
                        fig_s = igra.fig_v_str(fig)
                    %>
                        <img src="/static/{{fig_s}}.png"></img>
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
                        <input class="input" type="submit" name="click" value="{{x}}{{y}}">
                            % if fig != None:
                                <img src="/static/{{fig}}.png"></img>
                            % end
                    </div>
                % end
                % end
            </div>
            <div class="captured_pieces">
                <%
                for fig in igra.zajete_fig_beli:
                    fig_s = igra.fig_v_str(fig)
                %>
                    <img src="/static/{{fig_s}}.png"></img>
                % end
            </div>
        </div>
    </form>
</body>
</html>