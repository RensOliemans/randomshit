package beings.bodyParts

class Muscle(
        val limbOne: Limb = Limb(),
        val limbTwo: Limb = Limb(),
        var strength: Float = 0.0F
) {
    override fun toString(): String {
        return "Muscle(limbOne=$limbOne, limbTwo=$limbTwo, strength=$strength)"
    }
}