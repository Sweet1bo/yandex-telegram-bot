from orator.migrations import Migration


class CreatePhonesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('phones') as table:
            table.increments('id')
            table.integer('driver_id').unsigned()
            table.foreign('driver_id').references('id').on('drivers')
            table.string('phone', 20)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('phones')
