ai_commands = {'p1': {
                'mid-point': (499, 443),
                   'defense': (),
                   'attacked': (697, 171)

                },
               'p2': {
                   'mid-point': (615, 393),
                   'defense': (163, 446),
                   'attacked': (211, 444)
               },
               'p3': {
                   'mid-point': (691, 421),
                   'defense': (697, 688),
                   'attacked': (695, 645)
               },
               'p4': {
                   'mid-point': (736, 383),
                   'defense': (1232, 446),
                   'attacked': (1190, 445)
               },
}

class AI():
    def __init__(self, p1_units, p2_units, p3_units, p4_units, bases):
        self.p1 = [p1_units, 'p1']
        self.p2 = [p2_units, 'p2']
        self.p3 = [p3_units, 'p3']
        self.p4 = [p4_units, 'p4']
        self.bases = bases

        self.controlled = [self.p2, self.p3, self.p4]

        self.count = 0

    def update(self):


        for player in self.controlled:
            if len(player[0]) < 1:
                print(player, ' has died. Popping ', self.controlled.index(player))
                self.controlled.pop(self.controlled.index(player))
            for unit in player[0]:
                if unit not in self.bases:
                    if unit.attack_target == None:
                        # if len(player[0]) < 25:
                        #     for unit in player[0]:
                        #         if unit not in self.bases or unit not in player[0]:
                        #             unit.set_target(ai_commands[player[1]]['defense'])
                        #             unit.moving = True
                        #     continue

                        if len(player[0]) > len(self.p1[0]) + 10:
                            for unit in player[0]:
                                if unit not in self.bases or unit not in player[0]:
                                    unit.set_target(ai_commands['p1']['attacked'])
                                    unit.moving = True
                            continue

                        if len(player[0]) > len(self.p2[0]) + 10:
                            for unit in player[0]:
                                if unit not in self.bases or unit not in player[0]:
                                    unit.set_target(ai_commands['p2']['attacked'])
                                    unit.moving = True
                            continue

                        if len(player[0]) > len(self.p3[0]) + 10:
                            for unit in player[0]:
                                if unit not in self.bases or unit not in player[0]:
                                    unit.set_target(ai_commands['p3']['attacked'])
                                    unit.moving = True
                            continue
                        if len(player[0]) > len(self.p4[0]) + 10:
                            for unit in player[0]:
                                if unit not in self.bases or unit not in player[0]:
                                    unit.set_target(ai_commands['p3']['attacked'])
                                    unit.moving = True
                            continue


                        if len(player[0]) > 10:
                            count = 0
                            # while count < len(player[0]) //2:
                            for unit in player[0]:
                                if unit not in self.bases or unit not in player[0]:
                                    unit.set_target(ai_commands[player[1]]['mid-point'])
                                    unit.moving = True
                                    count += 1
                                # if count > len(player[0]) //2:
                                #     break
                            continue
                        for unit in player[0]:
                                if unit not in self.bases or unit not in player[0]:
                                    unit.set_target(ai_commands[player[1]]['defense'])
                                    unit.moving = True


