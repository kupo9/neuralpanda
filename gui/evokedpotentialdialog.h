#ifndef EVOKEDPOTENTIALDIALOG_H
#define EVOKEDPOTENTIALDIALOG_H

#include <QDialog>

namespace Ui {
class EvokedPotentialDialog;
}

class EvokedPotentialDialog : public QDialog
{
    Q_OBJECT

public:
    explicit EvokedPotentialDialog(QWidget *parent = 0);
    ~EvokedPotentialDialog();

private:
    Ui::EvokedPotentialDialog *ui;
};

#endif // EVOKEDPOTENTIALDIALOG_H
