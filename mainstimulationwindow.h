#ifndef MAINSTIMULATIONWINDOW_H
#define MAINSTIMULATIONWINDOW_H

#include <QMainWindow>

namespace Ui {
class MainStimulationWindow;
}

class MainStimulationWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainStimulationWindow(QWidget *parent = 0);
    ~MainStimulationWindow();

private:
    Ui::MainStimulationWindow *ui;
};

#endif // MAINSTIMULATIONWINDOW_H
