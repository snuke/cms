#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programming contest management system
# Copyright © 2012 Giovanni Mascellani <mascellani@poisson.phc.unipi.it>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import simplejson as json

from sqlalchemy import Column, ForeignKey, UniqueConstraint, CheckConstraint, \
     Boolean, Integer, String, Float, Interval
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import column_mapped_collection
from sqlalchemy.ext.orderinglist import ordering_list

from cms.db.SQLAlchemyUtils import Base


class Job(Base):
    __tablename__ = 'jobs'
    __mapper_args__ = {'polymorphic_on': 'type'}

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)

    # Input
    task_type = Column(String, nullable=False)
    task_type_parameters = Column(String, nullable=False)

    # Metadata
    shard = Column(String, nullable=True)
    sandboxes = Column(String, nullable=True)
    info = Column(String, nullable=False)


class CompilationJob(Job):
    __mapper_args__ = {'polymorphic_identity': 'compilation'}

    # Input
    language = Column(String, nullable=False)
    #files = {}
    #managers = {}

    # Output
    success = Column(Boolean, nullable=True)
    compilation_success = Column(Boolean, nullable=True)
    #executables = {}
    text = Column(String, nullable=True)
    plus = Column(String, nullable=True)

    @staticmethod
    def from_submission(submission):
        job = CompilationJob()

        # Job
        job.task_type = submission.task.task_type
        job.task_type_parameters = json.loads(
            submission.task.task_type_parameters)

        # CompilationJob
        job.language = submission.language
        job.files = submission.files
        job.managers = submission.task.managers
        job.info = "submission %d" % (submission.id)

        return job


class EvaluationJob(Job):
    __mapper_args__ = {'polymorphic_identity': 'evaluation'}

    # Input
    executables = {}
    testcases = {}
    time_limit = Column(Float, nullable=True)
    memory_limit = Column(Float, nullable=True)
    managers = {}
    files = {}

    # Output
    success = None
    evaluations = {}

    @staticmethod
    def from_submission(submission):
        job = EvaluationJob()

        # Job
        job.task_type = submission.task.task_type
        job.task_type_parameters = json.loads(
            submission.task.task_type_parameters)

        # EvaluationJob
        job.executables = submission.executables
        job.testcases = submission.task.testcases
        job.time_limit = submission.task.time_limit
        job.memory_limit = submission.task.memory_limit
        job.managers = submission.task.managers
        job.files = submission.files

        return job
