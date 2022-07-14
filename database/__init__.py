import datetime
import time
from flask import Flask, render_template, session, request, redirect, current_app, g
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, InputRequired
from flask_pagedown import PageDown
from flask_pagedown.fields import PageDownField
import os
from flask_sqlalchemy import SQLAlchemy
from .. import db


article_tag = db.Table('article_tag', db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
                       db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    url = db.Column(db.String(64))


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    subtitle = db.Column(db.String(64))
    post_time = db.Column(db.DateTime())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text())
    tags = db.relationship('Tag', secondary=article_tag, backref=db.backref('tag', ), lazy='immediate')
    year = db.Column(db.String(10))
    month = db.Column(db.String(10))


# article_category = db.Table('article_category', db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
#                             db.Column('category_id', db.Integer, db.ForeignKey('category.id')))


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    article = db.relationship('Article', backref='category', lazy='immediate')
    name = db.Column(db.String(64))

class Password(db.Model):
    __tablename__ = 'password'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64))
    password_hash = db.Column(db.String(300))