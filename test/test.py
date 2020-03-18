from app import Task
from app import db, app
import unittest
import os
import tempfile

# adapted from https://www.patricksoftwareblog.com/unit-testing-a-flask-application/
TEST_DB = 'test.db'

class Tests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        self.db_test, app.config["DATABASE"] = tempfile.mkstemp()
        app.testing = True
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        # app.config['TESTING'] = True
        # app.config['WTF_CSRF_ENABLED'] = False
        # app.config['DEBUG'] = False
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        #     os.path.join(app.config['BASEDIR'], TEST_DB)
        # self.app = app.test_client()
        # db.drop_all()
        # db.create_all()
        # self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def add(self, title, description, state):
        """
        Request to add a new task
        """
        return self.app.post('/add', data=dict(title=title,
                                               description=description,
                                               state=state),
                                     follow_redirects=True)
    def update_state(self, id, state):
        """
        Request to update the state of a task
        """
        return self.app.post('/update_state/' + str(id) + '/' + str(state),
                          data=dict(id=id, state=state),
                          follow_redirects=True)

    def delete(self, id):
        """
        Request to delete a task
        """
        return self.app.post('/delete/' + str(id), data=dict(id=id),
                           follow_redirects=True)

    def test_add(self):
        """
        Test if a task is added and is added properly
        """
        # add a todo
        self.add(title="Sample task todo", description="for sample", state="todo")
        task = Task.query.filter_by(title='Sample task todo').first()
        self.assertEqual(task.description, 'for sample')
        self.assertEqual(task.state, 'todo')

        # add a doing
        self.add(title="Sample task doing", description="for sample", state="doing")
        task = Task.query.filter_by(title="Sample task doing").first()
        self.assertEqual(task.description, 'for sample')
        self.assertEqual(task.state, 'doing')

        # add a done
        self.add(title="Sample task done", description="for sample", state="done")
        task = Task.query.filter_by(title='Sample task done').first()
        self.assertEqual(task.description, 'for sample')
        self.assertEqual(task.state, 'done')

    def test_update_state(self):
        """
        Test if a task's state can be updated
        """
        # add a task
        self.add(title="Sample task doing", description="for sample", state="doing")
        task = Task.query.filter_by(title='Sample task doing').first()

        # change task to todo
        old_id = task.id
        self.update_state(id=old_id, state='todo')
        task = Task.query.filter_by(title='Sample task doing').first()
        self.assertEqual(task.id, old_id)
        self.assertEqual(task.state, 'todo')

        # change task to done
        old_id = task.id
        self.update_state(id=old_id, state='done')
        task = Task.query.filter_by(title='Sample task doing').first()
        self.assertEqual(task.id, old_id)
        self.assertEqual(task.state, 'done')

    def test_delete(self):
        """
        Test if a task can be deleted
        """
        # add a task
        self.add(title="Sample task doing", description="for sample", state="doing")
        task = Task.query.filter_by(title='Sample task doing').first()

        # delete
        self.delete(id=task.id)
        task = Task.query.filter_by(title='Sample task doing').first()
        self.assertIsNone(task)

if __name__ == '__main__':
    unittest.main()
