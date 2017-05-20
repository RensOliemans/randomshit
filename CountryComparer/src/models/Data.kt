package models

import java.util.*

/**
 * Created by rens.
 */
class Country(
        var name: String = "",
        var continent: Continent? = null,
        var capital: City? = null,
        var size: Int = 0,
        var cities: MutableList<City> = ArrayList<City>(),
        var currency: String = "",
        var inetCode: String = "",
        var unIndex: Int = 0,
        var timeZone: Int = 0,
        var population: Map<Int, Long> = HashMap<Int, Long>(),
        var gdp: Map<Int, Long> = HashMap<Int, Long>(),
        var lifeExpectancy: Map<Int, Double> = HashMap<Int, Double>(),
        var unemploymentRate: Map<Int, Double> = HashMap<Int, Double>(),
        var henk: Set<City>
) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other?.javaClass != javaClass) return false

        other as Country

        if (name != other.name) return false

        return true
    }

    override fun toString(): String {
        return "Country(name='$name', continent=$continent, capital=$capital, size=$size, currency='$currency', population=$population)"
    }

    fun addCity(city: City) {
        if (!cities.contains(city)) {
            cities.add(city)
        }
    }

    fun addCities(cities: List<City>) {
        for (city in cities) addCity(city)
    }

    fun setCaptital(city: City) {
        addCity(city)
        capital = city
    }
}

class City(
        var name: String = "",
        var country: Country? = null,
        var population: Int = 0,
        var size: Int = 0,
        var timeZone: Int = 0
) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other?.javaClass != javaClass) return false

        other as City

        if (name != other.name) return false
        if (country != other.country) return false

        return true
    }

    override fun toString(): String {
        return "City(name='$name', country=$country, population=$population, size=$size, timeZone=$timeZone)"
    }

    fun getPopulation() {
        var i: Int = Calendar.getInstance().get(Calendar.YEAR)
        while (i > 0) {
            if (this.population)
        }
    }

}