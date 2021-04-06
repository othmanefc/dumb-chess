case class ScoreCount(
    score: Double,
    count: Double,
    sumBlackElo: Double,
    sumWhiteElo: Double
) {
  def add(other: ScoreCount): ScoreCount = {
    return ScoreCount(
      this.score + other.score,
      this.count + other.count,
      this.sumBlackElo + other.sumBlackElo,
      this.sumWhiteElo + other.sumBlackElo
    )
  }

  def asString(): String = {
    return this.score.toString() + "|" + this.count
      .toString() + "|" + this.sumBlackElo.toString() + "|" + this.sumWhiteElo
      .toString()
  }
}
