import java.util.ArrayList;
import java.util.List;

public class DouglasPeucker {

    public static List<Point> douglasPeucker(List<Point> pointList, double epsilon) {
        double dmax = 0;
        int index = 0;
        int end = pointList.size();

        for (int i = 2; i < end - 1; i++) {
            double d = perpendicularDistance(pointList.get(i), new Line(pointList.get(0), pointList.get(end - 1)));
            if (d > dmax) {
                index = i;
                dmax = d;
            }
        }

        List<Point> resultList = new ArrayList<>();

        if (dmax > epsilon) {
            List<Point> recResults1 = douglasPeucker(pointList.subList(0, index + 1), epsilon);
            List<Point> recResults2 = douglasPeucker(pointList.subList(index, end), epsilon);

            resultList.addAll(recResults1.subList(0, recResults1.size() - 1));
            resultList.addAll(recResults2);
        } else {
            resultList.add(pointList.get(0));
            resultList.add(pointList.get(end - 1));
        }

        return resultList;
    }

    private static double perpendicularDistance(Point point, Line line) {
        return 0.0;
    }

    public static void main(String[] args) {
        List<Point> inputPoints = new ArrayList<>();

        double epsilon = 0.1;

        List<Point> simplifiedPoints = douglasPeucker(inputPoints, epsilon);
    }
}
