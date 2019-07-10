package src.DesktopApp;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;
import javafx.scene.layout.StackPane;
import javafx.scene.input.DragEvent;
import javafx.scene.input.Dragboard;
import javafx.scene.input.TransferMode;
import javafx.event.EventHandler;
import javafx.concurrent.Task;
import javafx.stage.Stage;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class app extends Application {
    public static void main(String[] args) {
        launch(args);
    }
    
    @Override
    public void start(Stage primaryStage) throws Exception {
        Label label = new Label("Drag a file to me.");
        Label dropped = new Label("");
        VBox dragTarget = new VBox();
        dragTarget.getChildren().addAll(label,dropped);
        
        dragTarget.setOnDragOver(new EventHandler<DragEvent>() {
            @Override
            public void handle(DragEvent event) {
                if (event.getGestureSource() != dragTarget
                        && event.getDragboard().hasFiles()) {
                    /* allow for both copying and moving, whatever user chooses */
                    event.acceptTransferModes(TransferMode.COPY_OR_MOVE);
                }
                event.consume();
            }
        });

        dragTarget.setOnDragDropped(new EventHandler<DragEvent>() {
            @Override
            public void handle(DragEvent event) {
                Dragboard db = event.getDragboard();
                boolean success = false;
                if (db.hasFiles()) {
                    dropped.setText(db.getFiles().toString());
                    success = true;
                }
                /* let the source know whether the string was successfully 
                 * transferred and used */
                event.setDropCompleted(success);

                event.consume();
            }
        });


        StackPane root = new StackPane();
        root.getChildren().add(dragTarget);

        Scene scene = new Scene(root, 500, 250);

        primaryStage.setTitle("Drag Test");
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    // private final ExecutorService exec = Executors.newCachedThreadPool();

    // private String executeCommand(String command) {
    //     StringBuffer output = new StringBuffer();
    //     Process p;
    //     try {
    //         System.out.println(command);
    //         p = Runtime.getRuntime().exec(command);
    //         p.waitFor();
    //         BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
    //         String line = "";
    //         while ((line = reader.readLine())!= null) {
    //             output.append(line + "\n");
    //         }
    //     } catch (Exception e) {
    //         e.printStackTrace();
    //     }
    //     return output.toString();
    // }

    // public void launchCommand(String inputDir, String outputDir) {
    //     String command = ".\\venv\\Scripts\\python.exe ./test.py -i " + inputDir + " -o " + outputDir;
    //     Task<String> commandTask = new Task<String>() {
    //         @Override
    //         protected String call() {
    //             return executeCommand(command);
    //         }
    //     };
    //     commandTask.setOnSucceeded(event -> {
    //         // this is executed on the FX Application Thread, 
    //         // so it is safe to update the UI here if you need
    //         System.out.println(commandTask.getValue());
    //     });
    //     commandTask.setOnFailed(event -> {
    //         commandTask.getException().printStackTrace();
    //     });
    //     exec.execute(commandTask);

    // }
}