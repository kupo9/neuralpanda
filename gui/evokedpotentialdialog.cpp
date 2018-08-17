#include "evokedpotentialdialog.h"
#include "ui_evokedpotentialdialog.h"

EvokedPotentialDialog::EvokedPotentialDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::EvokedPotentialDialog)
{
    ui->setupUi(this);
}

EvokedPotentialDialog::~EvokedPotentialDialog()
{
    delete ui;
}
