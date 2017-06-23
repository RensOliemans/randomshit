package models

import java.util.*
import kotlin.collections.HashMap

/**
 * Created by rens.
 */

open class Place (
        var name: String = "",
        var size: Int = 0,
        var population: MutableMap<Int, Long> = HashMap<Int, Long>(),
        var timezone: Int = 0,
        var gdp: MutableMap<Int, Long> = HashMap<Int, Long>(),
        var lifeExpectancy: MutableMap<Int, Double> = HashMap<Int, Double>(),
        var unemploymentRate: MutableMap<Int, Double> = HashMap<Int, Double>()
) {
    fun getPopulation (year: Int = Calendar.getInstance().get(Calendar.YEAR)): Long? {
        var i = year
        while (i > 0) {
            if (this.population.containsKey(i)) {
                return this.population.get(i)
            }
            i--
        }
        return null
    }
    fun setPopulation(population: Long, year: Int = Calendar.getInstance().get(Calendar.YEAR)) {
        if (this.population.containsKey(year)) {
            this.population.remove(year)
        }
        this.population.put(year, population)
    }

    fun getGDP (year: Int = Calendar.getInstance().get(Calendar.YEAR)): Long? {
        var i = year
        while (i > 0) {
            if (this.gdp.containsKey(i)) {
                return this.gdp.get(i)
            }
            i--
        }
        return null
    }
    fun setGDP (gdp: Long, year: Int = Calendar.getInstance().get(Calendar.YEAR)) {
        if (this.gdp.containsKey(year)) {
            this.gdp.remove(year)
        }
        this.gdp.put(year, gdp)
    }

    fun getLifeExpectancy (year: Int = Calendar.getInstance().get(Calendar.YEAR)): Double? {
        var i = year
        while (i > 0) {
            if (this.lifeExpectancy.containsKey(i)) {
                return this.lifeExpectancy.get(i)
            }
            i--
        }
        return null
    }
    fun setLifeExpectancy (lifeExpectancy: Double, year: Int = Calendar.getInstance().get(Calendar.YEAR)) {
        if (this.lifeExpectancy.containsKey(year)) {
            this.lifeExpectancy.remove(year)
        }
        this.lifeExpectancy.put(year, lifeExpectancy)
    }

    fun getUnemploymentRate (year: Int = Calendar.getInstance().get(Calendar.YEAR)): Double? {
        var i = year
        while (i > 0) {
            if (this.unemploymentRate.containsKey(i)) {
                return this.unemploymentRate.get(i)
            }
            i--
        }
        return null
    }
    fun setUnemploymentRate (unemploymentRate: Double, year: Int = Calendar.getInstance().get(Calendar.YEAR)) {
        if (this.unemploymentRate.containsKey(year)) {
            this.unemploymentRate.remove(year)
        }
        this.unemploymentRate.put(year, unemploymentRate)
    }
}


class Country (
        var continent: Continent? = null,
        var capital: City? = null,
        var cities: MutableList<City> = ArrayList<City>(),
        var currency: String = "",
        var inetCode: String = "",
        var unIndex: Int = 0
) : Place() {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other?.javaClass != javaClass) return false

        other as Country

        if (name != other.name) return false

        return true
    }

    override fun hashCode(): Int{
        var result = name.hashCode()
        result = 31 * result + (continent?.hashCode() ?: 0)
        result = 31 * result + (capital?.hashCode() ?: 0)
        result = 31 * result + size
        result = 31 * result + cities.hashCode()
        result = 31 * result + currency.hashCode()
        result = 31 * result + inetCode.hashCode()
        result = 31 * result + unIndex
        result = 31 * result + population.hashCode()
        result = 31 * result + gdp.hashCode()
        result = 31 * result + lifeExpectancy.hashCode()
        result = 31 * result + unemploymentRate.hashCode()
        return result
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
        var country: Country? = null
) : Place() {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other?.javaClass != javaClass) return false

        other as City

        if (name != other.name) return false
        if (country != other.country) return false

        return true
    }

    override fun toString(): String {
        return "City(name='$name', country=$country, population=$population, size=$size)"
    }

    override fun hashCode(): Int{
        var result = name.hashCode()
        result = 31 * result + (country?.hashCode() ?: 0)
        result = 31 * result + population.hashCode()
        result = 31 * result + size
        return result
    }
}

class Continent(
        var countries: MutableList<City> = ArrayList<City>()
) : Place() {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other?.javaClass != javaClass) return false

        other as Continent

        if (name != other.name) return false

        return true
    }

    override fun hashCode(): Int {
        return name.hashCode()
    }



    fun addCountry(city: City) {
        if (!this.countries.contains(city)) {
            this.countries.add(city)
        }
    }

    override fun toString(): String {
        return "Continent(countries=$countries)"
    }
}
