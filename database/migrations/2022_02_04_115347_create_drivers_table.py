from orator.migrations import Migration


class CreateDriversTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('drivers') as table:
            table.increments('id')
            table.string('driver_id', 64).unique()
            table.string('car_id', 64).nullable()
            table.integer('park_id').unsigned()
            table.foreign('park_id').references('id').on('parks')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('drivers')
