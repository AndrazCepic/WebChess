<!DOCTYPE html>
<html>
<head>
    <title>Spletni Šah</title>
    <link rel="stylesheet" href="/static/main.css">
</head>
<body>
    <div class="header">
        % if not vel_pot:
            <h1>Klik je bil na </h1>
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
                        % if fig != None:
                            <img src="/static/{{fig}}.png"></img>
                        % end
                    <input class="square_input" type="submit" name="click" value="{{x}}{{y}}">
                </div>
            % end
            % end
        </div>
    </form>
</body>
</html>