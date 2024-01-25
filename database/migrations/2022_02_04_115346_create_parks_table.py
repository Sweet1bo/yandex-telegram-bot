from orator.migrations import Migration


class CreateParksTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('parks') as table:
            table.increments('id')
            table.string('name', 191)
            table.string('city', 191)
            table.string('park_id', 64).unique()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('parks')
