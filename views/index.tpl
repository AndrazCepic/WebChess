<!DOCTYPE html>
<html>
<head>
    <title>Spletni Šah</title>
    <link rel="stylesheet" href="/static/main.css">
</head>
<body>
    <div class="header">
        % if len(debug_str) != 0:
            <h1>DEBUG: {{debug_str}}</h1>
        % end
        % if not vel_pot:
            <h1>Poteza ni veljavna!</h1>
        % end
    </div>

    <form action="/board_input" method="POST">
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
                    <input class="square_input" type="submit" name="click" value="{{x}}{{y}}">
                    % if fig != None:
                        <img src="/static/{{fig}}.png"></img>
                    % end
                </div>
            % end
            % end
        </div>
    </form>
</body>
</html>