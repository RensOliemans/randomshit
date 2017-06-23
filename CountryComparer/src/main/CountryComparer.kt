package main

import models.City
import models.Continent
import models.Country

/**
 * Created by rens.
 */

fun main(args: Array<String>) {
    println("test")
    val europe = Continent();
    val netherlands = Country(europe)
    netherlands.name = "Netherlands"
    val amsterdam = City(netherlands)
    amsterdam.name = "Amsterdam"
    amsterdam.setPopulation(800000)
    print(amsterdam)
}
