def risky(temp, soil):
    """Finds a risk value based on the current data"""
    #Clone of risk calculation model from microbit
    risk = 0
    # Accepts half the risk to be the same as the soil moisture level. BR 2
    risk += 0.5 - 0.5 * (min(soil, 80) / 80)
    # Renders a risk degree suitable to the survivability of C. Brunneus in variable temperature ranges. BR 2
    if temp > 30:
        risk += 0.5
    elif temp > 20 and temp <= 30:
        risk += -0.2
    else:
        risk += 0.5
    # if not self.core.modelling:
    #     risk = (self.core.diogenic[0]/(self.core.vis_mult*100))-1
    print(f"{[round(soil, 2),round(temp, 2),round(risk, 2)]}")
    if risk < 0.2:
        final = "Low"
    elif risk >= 0.2 and risk <= 0.7:
        final = "Medium"
    else:
        final = "High"
    print(f"Risk Assessed as: {final}")
    return [round(risk, 2), final]

def test_risky():
    risk, final = risky(0, 50)
    assert risk == 0.69
    assert final == "Medium"
    risk, final = risky(10, 50)
    assert risk == 0.69
    assert final == "Medium"
    risk, final = risky(20, 50)
    assert risk == 0.69
    assert final == "Medium"
    risk, final = risky(23, 50)
    assert risk == -0.01
    assert final == "Low"
    risk, final = risky(27, 50)
    assert risk == -0.01
    assert final == "Low"
    risk, final = risky(30, 50)
    assert risk == -0.01
    assert final == "Low"
    risk, final = risky(40, 50)
    assert risk == 0.69
    assert final == "Medium"

# test_risky()