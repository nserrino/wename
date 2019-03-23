install:
	git clone https://github.com/TimeMagazine/babynames.git time-babynames
	cd time-babynames && npm install && cd ..

clean:
	rm -rf time-babynames