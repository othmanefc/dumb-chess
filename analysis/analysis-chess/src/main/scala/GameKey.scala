case class GameKey(
    opening: String,
    eco: String,
    tempo: String,
    avgEloClass: String,
    ratingDiff: String
) {
  def asString(): String = {
    return this.opening + "|" + this.eco + "|" + this.tempo + "|" + this.avgEloClass + "|" + this.ratingDiff;
  }
}
