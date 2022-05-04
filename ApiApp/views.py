from django.shortcuts import render
import datetime
# Create your views here.
from django.contrib.auth.hashers import make_password,get_hasher

from rest_framework.generics import ListCreateAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .loader import *

class AllBookView(ListCreateAPIView):
    queryset = Book.objects.all().order_by("-id")
    serializer_class = LoaderBook
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        auth = request.user
        name = request.POST['name']
        file = request.FILES['file']
        lang = Language.objects.get(id=request.POST['lang'])       
        img = request.FILES['img']
        date = datetime.datetime.today()
        category = Category.objects.get(id=request.POST['category'])
        text = request.POST['text']
        book = Book.objects.create(
            auth=auth,
            category=category,
            lang=lang,
            file=file,
            img=img,
            date=date,
            name=name,
            text=text,
            )
        ser = self.serializer_class(book)
        return Response(ser.data)


class AllAudioBookView(ListCreateAPIView):
    queryset = AudioBook.objects.all().order_by("-id")
    serializer_class = LoaderAudioBook
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        auth = request.user
        name = request.POST['name']
        file = request.FILES['file']
        lang = Language.objects.get(id=request.POST['lang'])       
        img = request.FILES['img']
        date = datetime.datetime.today()
        category = Category.objects.get(id=request.POST['category'])
        text = request.POST['text']
        book = AudioBook.objects.create(
            auth=auth,
            category=category,
            lang=lang,
            file=file,
            img=img,
            date=date,
            name=name,
            text=text,
            )
        ser = self.serializer_class(book)
        return Response(ser.data)


class OneBookView(ListAPIView):
    queryset = Book.objects.all().order_by("-id")
    serializer_class = LoaderBook
    permission_classes = (IsAuthenticated,)
    
    def get(self,request,pk:int):
        item = Book.objects.get(id=pk)
        serializer = self.serializer_class(item)
        data = serializer.data
        another_books = Book.objects.filter(auth=item.auth)
        another_ser = self.serializer_class(another_books,many=True)
        data['another'] = another_ser.data
        return Response(data)

class OneAudioBookView(ListAPIView):
    queryset = AudioBook.objects.all().order_by("-id")
    serializer_class = LoaderAudioBook
    permission_classes = (IsAuthenticated,)
    
    def get(self,request,pk:int):
        item = AudioBook.objects.get(id=pk)
        serializer = self.serializer_class(item)
        data = serializer.data
        another_books = AudioBook.objects.filter(auth=item.auth)
        another_ser = self.serializer_class(another_books,many=True)
        data['another'] = another_ser.data
        return Response(data)

class RatingAudioBookAddView(ListCreateAPIView):
    queryset = AudioBook.objects.all().order_by("-id")
    serializer_class = LoaderReytingAudioBook
    permission_classes = (IsAuthenticated,)

    def post(self,request,pk):
        user = request.user
        book = AudioBook.objects.get(id=pk)
        star = request.POST['star']
        check = ReytingAudioBook.objects.filter(auth=user)
        if len(check) > 0:
            old = check[0].star
            check[0].star = star 
            check[0].save()
            book.reyting -= old
            book.reyting += int(star)
            book.save()
            ser = self.serializer_class(check[0])
        else:
            new = ReytingAudioBook.objects.create(auth=user,star=star,book=book)
            ser = self.serializer_class(new)
            book.reyting_count += 1
            book.reyting += int(star)
            book.save()

        return Response(ser.data)

class RatingBookAddView(ListCreateAPIView):
    queryset = Book.objects.all().order_by("-id")
    serializer_class = LoaderReytingBook
    permission_classes = (IsAuthenticated,)

    def post(self,request,pk):
        user = request.user
        book = Book.objects.get(id=pk)
        star = request.POST['star']
        check = ReytingBook.objects.filter(auth=user)
        if len(check) > 0:
            old = check[0].star
            check[0].star = star
            book.reyting -= old
            book.reyting += int(star)
            book.save() 
            check[0].save()
            ser = self.serializer_class(check[0])

        else:
            new = ReytingBook.objects.create(auth=user,star=star,book=book)
            ser = self.serializer_class(new)
            book.reyting_count += 1
            book.reyting += int(star)
            book.save()

        return Response(ser.data)

class RecomendedBookView(ListAPIView):
    queryset = Book.objects.filter(reyting__gte=1,reyting__lte=5)
    serializer_class = LoaderBook
    permission_classes = (IsAuthenticated,)

class RecomendedAudioBookView(ListAPIView):
    queryset = AudioBook.objects.filter(reyting__gte=1,reyting__lte=5)
    serializer_class = LoaderAudioBook
    permission_classes = (IsAuthenticated,)

class LoginRegister(ListCreateAPIView):
    queryset = Client.objects.all()
    
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        full_name = request.POST['full_name']
        try:
            user = Client.objects.create(username=username,password=make_password(password),email=email,full_name=full_name)
            data = {
                "username":username,
                "email":email,
                "password":user.password,
                "full_name":full_name
            }
            return Response(data)
        except Exception as error:
            print(error)
            return Response({"error":True},status=401)

class GoingToReadAdd(ListCreateAPIView):
    queryset = HistoryBook.objects.all()
    serializer_class = LoaderHistoryBook
    permission_classes = (IsAuthenticated,)

    def post(self,request):
            book = request.POST['book']
            book = Book.objects.get(id=book)
            user = request.user
            check = HistoryBook.objects.filter(book=book,user=user,types=1)
            if len(check) <= 0:
                hs = HistoryBook.objects.create(types=1,book=book,user=user)
                ser = self.serializer_class(hs)
                return Response(ser.data)
            else:
                return Response({"error":True})

    def get(self,request):
        user = request.user
        data = self.serializer_class(HistoryBook.objects.filter(user=user,types=1),many=True).data
        return Response(data)

class ReadingAdd(ListCreateAPIView):
    queryset = HistoryBook.objects.all()
    serializer_class = LoaderHistoryBook
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        book = request.POST['book']
        book = Book.objects.get(id=book)
        user = request.user
        check = HistoryBook.objects.filter(book=book,user=user,types=2)
        if len(check) <= 0:
            hs = HistoryBook.objects.create(types=2,book=book,user=user)
            ser = self.serializer_class(hs)
            return Response(ser.data)
        else:
            return Response({"error":True})

    def get(self,request):
        user = request.user
        data = self.serializer_class(HistoryBook.objects.filter(user=user,types=2),many=True).data
        return Response(data)

class ReadedAdd(ListCreateAPIView):
    queryset = HistoryBook.objects.all()
    serializer_class = LoaderHistoryBook
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        book = request.POST['book']
        book = Book.objects.get(id=book)
        user = request.user
        check = HistoryBook.objects.filter(book=book,user=user,types=3)
        if len(check) <= 0:
            hs = HistoryBook.objects.create(types=3,book=book,user=user)
            ser = self.serializer_class(hs)
            return Response(ser.data)
        else:
            return Response({"error":True})

    def get(self,request):
        user = request.user
        data = self.serializer_class(HistoryBook.objects.filter(user=user,types=3),many=True).data
        return Response(data)




class GoingToReadAudioAdd(ListCreateAPIView):
    queryset = HistoryAudioBook.objects.all()
    serializer_class = LoaderHistoryAudioBook
    permission_classes = (IsAuthenticated,)

    def post(self,request):
            book = request.POST['book']
            book = AudioBook.objects.get(id=book)
            user = request.user
            check = HistoryAudioBook.objects.filter(book=book,user=user,types=1)
            if len(check) <= 0:
                hs = HistoryAudioBook.objects.create(types=1,book=book,user=user)
                ser = self.serializer_class(hs)
                return Response(ser.data)
            else:
                return Response({"error":True})

    def get(self,request):
        user = request.user
        data = self.serializer_class(HistoryAudioBook.objects.filter(user=user,types=1),many=True).data
        return Response(data)

class ReadingAudioAdd(ListCreateAPIView):
    queryset = HistoryAudioBook.objects.all()
    serializer_class = LoaderHistoryAudioBook
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        book = request.POST['book']
        book = AudioBook.objects.get(id=book)
        user = request.user
        check = HistoryAudioBook.objects.filter(book=book,user=user,types=2)
        if len(check) <= 0:
            hs = HistoryAudioBook.objects.create(types=2,book=book,user=user)
            ser = self.serializer_class(hs)
            return Response(ser.data)
        else:
            return Response({"error":True})

    def get(self,request):
        user = request.user
        data = self.serializer_class(HistoryAudioBook.objects.filter(user=user,types=2),many=True).data
        return Response(data)

class ReadedAudioAdd(ListCreateAPIView):
    queryset = HistoryAudioBook.objects.all()
    serializer_class = LoaderHistoryAudioBook
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        book = request.POST['book']
        book = AudioBook.objects.get(id=book)
        user = request.user
        check = HistoryAudioBook.objects.filter(book=book,user=user,types=3)
        if len(check) <= 0:
            hs = HistoryAudioBook.objects.create(types=3,book=book,user=user)
            ser = self.serializer_class(hs)
            return Response(ser.data)
        else:
            return Response({"error":True})

    def get(self,request):
        user = request.user
        data = self.serializer_class(HistoryAudioBook.objects.filter(user=user,types=3),many=True).data
        return Response(data)

class SearchAudioBook(ListAPIView):
    queryset = AudioBook.objects.all()
    serializer_class = LoaderAudioBook
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        search = request.GET['search']
        item = AudioBook.objects.filter(name__icontains=search)
        ser = self.serializer_class(item,many=True)
        return Response(ser.data)

class SearchBook(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = LoaderBook
    permission_classes = (IsAuthenticated,)
    
    def get(self,request):
        search = request.GET['search']
        item = Book.objects.filter(name__icontains=search)
        ser = self.serializer_class(item,many=True)
        return Response(ser.data)

class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = LoaderCategory
    permission_classes = (IsAuthenticated,)


class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = LoaderCategory
    permission_classes = (IsAuthenticated,)

    def get(self,request,pk):
        category = Category.objects.get(id=pk)
        A_items = LoaderAudioBook(AudioBook.objects.filter(category=category),many=True)
        S_items = LoaderBook(Book.objects.filter(category=category),many=True)
        data = [A_items.data,S_items.data]
        return Response(data)
