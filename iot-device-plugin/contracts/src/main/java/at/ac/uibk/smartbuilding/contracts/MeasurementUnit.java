package at.ac.uibk.smartbuilding.contracts;

public enum MeasurementUnit {
    // Base SI units
    METER("Meter", "m"),
    KILOGRAM("Kilogram", "kg"),
    SECOND("Second", "s"),
    AMPERE("Ampere", "A"),
    KELVIN("Kelvin", "K"),
    MOLE("Mole", "mol"),
    CANDELA("Candela", "cd"),

    // Derived SI units
    HERTZ("Hertz", "Hz"),
    NEWTON("Newton", "N"),
    PASCAL("Pascal", "Pa"),
    JOULE("Joule", "J"),
    WATT("Watt", "W"),
    COULOMB("Coulomb", "C"),
    VOLT("Volt", "V"),
    FARAD("Farad", "F"),
    OHM("Ohm", "Ω"),
    SIEMENS("Siemens", "S"),
    WEBER("Weber", "Wb"),
    TESLA("Tesla", "T"),
    HENRY("Henry", "H"),
    DEGREE_CELSIUS("Degree Celsius", "°C"),
    LUMEN("Lumen", "lm"),
    LUX("Lux", "lx"),
    BECQUEREL("Becquerel", "Bq"),
    GRAY("Gray", "Gy"),
    SIEVERT("Sievert", "Sv"),
    KATAL("Katal", "kat"),

    HUMIDITY("Relative Humidity", "%");


    private final String unitName;
    private final String abbreviation;

    MeasurementUnit(String unitName, String abbreviation) {
        this.unitName = unitName;
        this.abbreviation = abbreviation;
    }

    public String getUnitName() {
        return unitName;
    }

    public String getAbbreviation() {
        return abbreviation;
    }
}

