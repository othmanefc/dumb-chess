import org.apache.spark.sql.SparkSession
import org.apache.spark.SparkConf
import org.apache.spark.api.java.{JavaPairRDD, JavaRDD, JavaSparkContext}
import scala.collection.JavaConverters._
import scala.util.Sorting._
import java.io._

object ChessMiner {
  def main(args: Array[String]): Unit = {
    val pgnFile: String = "games/Kasparov.pgn";
    val spark = SparkSession
      .builder()
      .master("local")
      .appName("Chess analysis")
      .getOrCreate();
    val df = spark.read.textFile(pgnFile).cache();
    val whiteWin: Long = df.filter((x: String) => x.contains("1-0")).count();
    val blackWin: Long = df.filter((x: String) => x.contains("0-1")).count();
    val draw: Long = df.filter((x: String) => x.contains("1/2-1/2")).count();

    df.printSchema()
    println(s"White wins: $whiteWin");
    println(s"Black wins: $blackWin");
    println(s"Draw: $draw");

    spark.stop();

    val bigFile: String = "games/lichess_db_standard_rated_2018-02.pgn";
    processPGNFile(bigFile)

  }

  def processPGNFile(file: String): Unit = {
    val conf = new SparkConf().setAppName("Chess analysis").setMaster("local");
    val sc = new JavaSparkContext(conf);
    sc.setLogLevel("INFO");
    sc.hadoopConfiguration.set("textinputformat.record.delimiter", "[Event");
    var pgnData = sc.textFile(file);
    pgnData = pgnData.filter(line => line.length > 1);

    computeGameStats(pgnData);
    sc.stop();

  }

  def computeGameStats(pgnfile: JavaRDD[String]) = {
    val openingToGameScore: JavaPairRDD[GameKey, ScoreCount] = pgnfile
      .mapToPair(game =>
        (
          createGameKey(game),
          ScoreCount(getScore(game), 1, getWhiteElo(game), getBlackElo(game))
        )
      )
      .reduceByKey((score1, score2) => score1.add(score2));

    val analyzedOpenings: List[Tuple2[GameKey, ScoreCount]] =
      openingToGameScore.collect().asScala.toList;

    stableSort(
      analyzedOpenings,
      (_._2.count < _._2.count): (
          (GameKey, ScoreCount),
          (GameKey, ScoreCount)
      ) => Boolean
    )

    saveToFile(analyzedOpenings, "openingsFile")

  }

  def createGameKey(game: String): GameKey = {
    val ret = GameKey(
      getOpening(game),
      getPgnField(game, "ECO"),
      getSpeedMode(game),
      getAvgEloClass(game),
      getRatingDiff(game)
    );
    return ret
  }

  def getWhiteElo(game: String): Double = {
    val whiteElo: String = getPgnField(game, "WhiteElo");
    if (whiteElo.contains("???")) {
      return 0;
    }
    return whiteElo.toDouble
  }

  def getBlackElo(game: String): Double = {
    val blackElo: String = getPgnField(game, "BlackElo");
    if (blackElo.contains("???")) {
      return 0;
    }
    return blackElo.toDouble
  }

  def getRatingDiff(game: String): String = {
    val whiteElo = getWhiteElo(game);
    val blackElo = getBlackElo(game);
    if (whiteElo == 0 || blackElo == 0) {
      return "???";
    }
    val diff: Double = (whiteElo - blackElo).abs
    val stronger: String = if (whiteElo > blackElo) "Whitel" else "Black";

    diff match {
      case x if x < 100 => return "White=Black"
      case x if x < 300 => return stronger + "+200"
      case x if x < 500 => return stronger + "+400"
      case _            => return stronger + "+500+"
    }
  }

  def getAvgEloClass(game: String): String = {
    val whiteElo = getWhiteElo(game);
    val blackElo = getBlackElo(game);
    if (whiteElo == 0 || blackElo == 0) {
      return "???";
    }

    val average: Double = (whiteElo + blackElo) / 2;
    if (average < 1200) {
      return "0-1199";
    } else if (average < 1400) {
      return "1200-1399";
    } else if (average < 1600) {
      return "1400-1599";
    } else if (average < 1800) {
      return "1600-1799";
    } else if (average < 2000) {
      return "1800-1999";
    } else if (average < 2200) {
      return "2000-2199";
    } else if (average < 2400) {
      return "2200-2399";
    } else
      return "2400+";
  }

  def getSpeedMode(game: String): String = {
    val speed = game.substring(0, game.indexOf("]"));
    speed match {
      case x if x.contains("UltraBullet") => return "UltraBullet"
      case x if x.contains("Bullet")      => return "Bullet"
      case x if x.contains("Blitz")       => return "Blitz"
      case x if x.contains("Classical")   => return "Classical"
      case _                              => return "???"
    }
  }

  def getOpening(game: String): String = {
    return getPgnField(game, "Opening")
  }

  def getScore(game: String): Double = {
    if (game.contains("1-0")) {
      return 1;
    } else if (game.contains("1/2-1/2")) {
      return 0.5;
    } else { return 0 }
  }

  def getPgnField(game: String, field: String): String = {
    var pgn = game.substring(game.indexOf(field));
    pgn = pgn.substring(pgn.indexOf("\"") + 1);
    pgn = pgn.substring(0, pgn.indexOf("\""));
    if (pgn.contains("\n")) {
      return "???";
    }
    return pgn
  }

  def saveToFile(
      openings: List[Tuple2[GameKey, ScoreCount]],
      filename: String
  ) {
    val file = new File(filename)
    val bw = new BufferedWriter(new FileWriter(file))
    println("Saving")
    bw.write(
      classOf[GameKey].getDeclaredFields
        .map(_.getName)
        .toList
        .mkString(
          "|"
        ) + "|" + classOf[ScoreCount].getDeclaredFields
        .map(_.getName)
        .toList
        .mkString("|" + "\n")
    )
    for (tuple <- openings) {
      bw.write(tuple._1.asString() + "|" + tuple._2.asString() + "\n");
    }
    bw.close()
  }
}
