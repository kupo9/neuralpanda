#include "mainstimulationwindow.h"
#include "ui_mainstimulationwindow.h"

MainStimulationWindow::MainStimulationWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainStimulationWindow)
{
    ui->setupUi(this);
}

MainStimulationWindow::~MainStimulationWindow()
{
    delete ui;
}

