package beings

import beings.bodyParts.Muscle

interface AbstractMammalBeing : AbstractBeing {
    /*
    This class is an interface of a mammal. It extends AbstractBeing (since all beings extend AbstractBeing),
    and has a couple of unique features. These are:
     */
    val amountOfLimbs: Int
    val muscles: List<Muscle>
}
